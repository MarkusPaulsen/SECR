# <editor-fold desc="Import typing">
from typing import *
# </editor-fold>
# <editor-fold desc="Import RxPY">
from rx import from_list
from rx.operators import to_list, map, filter
# </editor-fold>
# <editor-fold desc="Import other classes">
from simpletransformers.classification import ClassificationModel
# </editor-fold>

# <editor-fold desc="Import own classes">
from Productive.Model.Document import Document
from Productive.Model.Sentence import Sentence
# </editor-fold>


# noinspection PyMethodMayBeStatic
class TermLabelLayer:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._term_label_args: dict = self._setup_term_label_args()
        self._term_label_model: ClassificationModel = self._setup_term_label_model()
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def apply_word_seperation(self, document: Document):
        (
            from_list(document.get_sentences())
            .pipe(filter(lambda sentence: sentence.get_relevant()))
            .subscribe(lambda sentence: sentence.set_words(list(set(sentence.get_sentence().split(" ")))))
        )

    def apply_term_label(self, document: Document):
        (
            from_list(document.get_sentences())
            .pipe(filter(lambda sentence: sentence.get_words() != []))
            .subscribe(lambda sentence: self._apply_term_label_sentence(sentence=sentence))
        )
    # </editor-fold>

    # <editor-fold desc="Classification method">
    def _classify_term(self, word: str) -> Tuple[str, str]:
        predictions, raw_outputs = self._term_label_model.predict([word])
        if predictions == 0:
            label_type = "Action"
        elif predictions == 1:
            label_type = "Modifier"
        elif predictions == 2:
            label_type = "Object"
        elif predictions == 3:
            label_type = "Subject"
        else:
            label_type = "Error in classify_term()"

        return word, label_type

    def _apply_term_label_sentence(self, sentence: Sentence):
        term_annotated_words = (
            from_list(sentence.get_words())
            .pipe(map(lambda word: self._classify_term(word)))
            .pipe(to_list())
            .run()
        )
        sentence.set_term_annotated_words(term_annotated_words=term_annotated_words)
    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_term_label_args(self) -> dict:
        return {
            "reprocess_input_data": True,
            "overwrite_output_dir": True,
            "use_cached_eval_features": True,
            "evaluate_during_training": True,
            "max_seq_length": 128,
            "num_train_epochs": 5,
            "evaluate_during_training_steps": 1000,
            "save_model_every_epoch": False,
            "save_eval_checkpoints": False,
            "train_batch_size": 64,
            "eval_batch_size": 64,
        }

    def _setup_term_label_model(self) -> ClassificationModel:
        return ClassificationModel(
            model_type="roberta",
            model_name="../Resources/term_label_model",
            num_labels=4,
            args=self._term_label_args,
            use_cuda=False
        )
    # </editor-fold>
