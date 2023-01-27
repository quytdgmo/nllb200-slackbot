import sys
from typing import List
from functools import lru_cache

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import torch

DEF_MAX_SRC_CHARS = 512
DEF_MAX_TGT_LEN = 512
DEF_MODEL_ID = "facebook/nllb-200-distilled-600M"
DEF_SRC_LNG = 'jpn_Jpan'
DEF_TGT_LNG = 'vie_Latn'

device = torch.device(torch.cuda.is_available() and 'cuda' or 'cpu')

class Translator:
    def __init__(self, model_id, logger):
        if model_id is None:
            model_id = DEF_MODEL_ID
        self.model_id = model_id
        self.logger = logger
        self.logger.info(f'torch device={device}')
        self.logger.info(f"Loading model {model_id} ...")
        self.model_dict = self.load_models()
        # self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to(device)
        #
        # self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        # src_langs = tokenizer.additional_special_tokens

    def load_models(self):
        # build model and tokenizer
        model_name_dict = {'nllb-distilled-600M': 'facebook/nllb-200-distilled-600M',
                      #'nllb-1.3B': 'facebook/nllb-200-1.3B',
                      #'nllb-distilled-1.3B': 'facebook/nllb-200-distilled-1.3B',
                      #'nllb-3.3B': 'facebook/nllb-200-3.3B',
                      }

        model_dict = {}

        for call_name, real_name in model_name_dict.items():
            print('\tLoading model: %s' % call_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(real_name)
            tokenizer = AutoTokenizer.from_pretrained(real_name)
            model_dict[call_name+'_model'] = model
            model_dict[call_name+'_tokenizer'] = tokenizer

        return model_dict


    def translate(self, source, target, text):
        if len(self.model_dict) == 2:
            model_name = 'nllb-distilled-600M'

        start_time = time.time()

        model = model_dict[model_name + '_model']
        tokenizer = model_dict[model_name + '_tokenizer']

        translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target)
        output = translator(text, max_length=DEF_MAX_TGT_LEN)

        end_time = time.time()

        output = output[0]['translation_text']
        result = {'inference_time': end_time - start_time,
                  'source': source,
                  'target': target,
                  'result': output}
        return result
