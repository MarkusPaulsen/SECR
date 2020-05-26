from Productive.Controller.DeviceLayer import DeviceLayer
from Productive.Controller.EffectLayer import EffectLayer
from Productive.Controller.RelevanceLayer import RelevanceLayer
from Productive.Controller.TermLabelLayer import TermLabelLayer
from Productive.Model.Document import Document

rl = RelevanceLayer()
tl = TermLabelLayer()
el = EffectLayer()
dl = DeviceLayer()
document = Document("2019/Fireeye_rpt-apt41(08-07-2019).pdf")
rl.apply_relevance(document=document)
tl.apply_word_seperation(document=document)
tl.apply_relevance(document=document)
el.apply_effect(document=document)
dl.apply_device(document=document)

