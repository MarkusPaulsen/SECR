# <editor-fold desc="Import RX">
from rx import from_list
from simpletransformers.classification import ClassificationModel

from Productive.Model.Document import Document


# </editor-fold>


class RelevanceLayer:

    def __init__(self):
        self._relevance_args: dict = {
            "reprocess_input_data": True,
            "overwrite_output_dir": True,
            "use_cached_eval_features": True,
            "evaluate_during_training": True,
            "max_seq_length": 128,
            "num_train_epochs": 3,
            "evaluate_during_training_steps": 1000,
            "wandb_project": "tar-classification-model-comparison",
            "wandb_kwargs": {"name": 'test'},
            "save_model_every_epoch": False,
            "save_eval_checkpoints": False,
            "train_batch_size": 64,
            "eval_batch_size": 64,
        }
        self._relevance_model: ClassificationModel = ClassificationModel(
            "model_name",
            "model_directory",
            args=self._relevance_args,
            use_cuda=False
        )

    def _classify_relevance(self, sentence: str) -> bool:
        """
        raw_outputs: condidence array for each label
        :return: 0 if sentence is not relevant and 1 if relevant
        """
        predictions, raw_outputs = self._relevance_model.predict(sentence)
        return True if predictions else False

    def apply_relevance(self, document: Document):
        (
            from_list(document.get_sentences())
            .subscribe(lambda sentence: sentence.set_relevant(self._classify_relevance(sentence)))
        )
