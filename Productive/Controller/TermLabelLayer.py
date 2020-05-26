from typing import *
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list
# </editor-fold>
from simpletransformers.classification import ClassificationModel

from Productive.Model.Sentence import Sentence
from Productive.Model.Document import Document


# </editor-fold>


# noinspection PyMethodMayBeStatic
class TermLabelLayer:

    def __init__(self):
        self._type_args: dict = {
            "reprocess_input_data": True,
            "overwrite_output_dir": True,
            "use_cached_eval_features": True,
            "evaluate_during_training": True,
            "max_seq_length": 128,
            "num_train_epochs": 5,
            "evaluate_during_training_steps": 1000,
            "wandb_project": "tar-type-model-comparison",
            "wandb_kwargs": {"name": 'test'},
            "save_model_every_epoch": False,
            "save_eval_checkpoints": False,
            "train_batch_size": 64,
            "eval_batch_size": 64,
        }
        self._type_model: ClassificationModel = ClassificationModel(
            "model_name",
            "model_directory",
            num_labels=4,
            args=self._type_args,
            use_cuda=False
        )

    def _classify_term(self, word: str) -> Tuple[str, str]:
        predictions, raw_outputs = self._type_model.predict(word)
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

    def apply_word_seperation(self, document: Document):
        (
            from_list(document.get_sentences())
            .pipe(filter(lambda sentence: sentence.get_relevant()))
            .subscribe(lambda sentence: sentence.set_words(sentence.get_sentence().split(" ")))
        )

    def _apply_relevance_sentence(self, sentence: Sentence):
        term_annotated_words = (
            from_list(sentence.get_words())
            .pipe(map(lambda word: self._classify_term(word)))
            .pipe(to_list())
            .run()
        )
        sentence.set_term_annotated_words(term_annotated_words=term_annotated_words)

    def apply_relevance(self, document: Document):
        (
            from_list(document.get_sentences())
            .subscribe(lambda sentence: self._apply_relevance_sentence(sentence=sentence))
        )
