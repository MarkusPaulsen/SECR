# <editor-fold desc="Import RxPY">
from rx import from_list
# </editor-fold>
# <editor-fold desc="Import other classes">
from simpletransformers.classification import ClassificationModel
# </editor-fold>

# <editor-fold desc="Import own classes">
from Productive.Model.Document import Document
# </editor-fold>


class RelevanceLayer:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._relevance_args: dict = self._setup_relevance_args()
        self._relevance_model: ClassificationModel = self._setup_relevance_model()
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def apply_relevance(self, document: Document):
        (
            from_list(document.get_sentences())
            .subscribe(lambda sentence: sentence.set_relevant(self._classify_relevance(sentence.get_sentence())))
        )
    # </editor-fold>

    # <editor-fold desc="Classification methods">
    def _classify_relevance(self, sentence: str) -> bool:
        """
        raw_outputs: condidence array for each label
        :return: 0 if sentence is not relevant and 1 if relevant
        """
        predictions, raw_outputs = self._relevance_model.predict([sentence])
        return True if predictions[0] == 1 else False
    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_relevance_args(self) -> dict:
        return {
            "reprocess_input_data": True,
            "overwrite_output_dir": True,
            "use_cached_eval_features": True,
            "evaluate_during_training": True,
            "max_seq_length": 128,
            "num_train_epochs": 3,
            "evaluate_during_training_steps": 1000,
            "save_model_every_epoch": False,
            "save_eval_checkpoints": False,
            "train_batch_size": 64,
            "eval_batch_size": 64,
        }

    def _setup_relevance_model(self) -> ClassificationModel:
        return ClassificationModel(
            model_type="roberta",
            model_name="../Resources/relevance_model",
            args=self._relevance_args,
            use_cuda=False
        )
    # </editor-fold>
