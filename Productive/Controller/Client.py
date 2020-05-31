# <editor-fold desc="Description">
import sys
# </editor-fold>

# <editor-fold desc="Description">
from Productive.Model.Document import Document
from Productive.Controller.RelevanceLayer import RelevanceLayer
from Productive.Controller.TermLabelLayer import TermLabelLayer
from Productive.Controller.EffectLayer import EffectLayer
from Productive.Controller.DeviceLayer import DeviceLayer
from Productive.View.ViewLayer import ViewLayer
# </editor-fold>


class Client:

    # <editor-fold desc="Constructor">
    def __init__(self):
        if sys.argv is not None:
            if len(sys.argv) == 2:
                self._rl = RelevanceLayer()
                self._tl = TermLabelLayer()
                self._el = EffectLayer()
                self._dl = DeviceLayer()
                self._vl = ViewLayer()
                print("Loading document:", file=sys.stderr)
                document = Document(sys.argv[1])
                print("Estimating relevance:", file=sys.stderr)
                self._rl.apply_relevance(document=document)
                print("Separating sentences:", file=sys.stderr)
                self._tl.apply_word_seperation(document=document)
                print("Estimating term labels:", file=sys.stderr)
                self._tl.apply_term_label(document=document)
                print("Looking up effects:", file=sys.stderr)
                self._el.apply_effect(document=document)
                print("Looking up devices:", file=sys.stderr)
                self._dl.apply_device(document=document)
                print("Creating the view:", file=sys.stderr)
                self._vl.print_document(document=document)

            else:
                print("Wrong number of parameters provided!", file=sys.stderr)
        else:
            print("No parameters provided!", file=sys.stderr)
    # </editor-fold>


if __name__ == "__main__":
    Client()
