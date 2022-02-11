from typing import List

from common.request import Request, Sequence, Token
from .openai_token_counter import OpenAITokenCounter


class TestOpenAITokenCounter:

    # The following prompt has 51 tokens according to the GPT-2 tokenizer
    TEST_PROMPT: str = (
        "The Center for Research on Foundation Models (CRFM) is "
        "an interdisciplinary initiative born out of the Stanford "
        "Institute for Human-Centered Artificial Intelligence (HAI) "
        "that aims to make fundamental advances in the study, development, "
        "and deployment of foundation models."
    )

    def setup_method(self, method):
        self.token_counter = OpenAITokenCounter()

    def test_count_tokens(self):
        request = Request(prompt=TestOpenAITokenCounter.TEST_PROMPT)
        completions: List[Sequence] = [
            Sequence(
                text=" The CRFM is dedicated to advancing our knowledge of the foundations of artificial intelligence "
                "(AI) and related fields. It focuses on foundational questions in AI, which are",
                logprob=-49.00783279519999,
                tokens=[
                    Token(text=" The", logprob=-1.8096403, top_logprobs={"\n": -1.6654028}),
                    Token(text=" CR", logprob=-1.2861944, top_logprobs={" CR": -1.2861944}),
                    Token(text="FM", logprob=-0.0032369632, top_logprobs={"FM": -0.0032369632}),
                    Token(text=" is", logprob=-1.4355252, top_logprobs={" is": -1.4355252}),
                    Token(text=" dedicated", logprob=-3.814422, top_logprobs={" a": -1.8003343}),
                    Token(text=" to", logprob=-0.009623392, top_logprobs={" to": -0.009623392}),
                    Token(text=" advancing", logprob=-2.6732886, top_logprobs={" the": -1.859751}),
                    Token(text=" our", logprob=-3.123714, top_logprobs={" the": -1.0504603}),
                    Token(text=" knowledge", logprob=-3.030337, top_logprobs={" understanding": -0.34646907}),
                    Token(text=" of", logprob=-0.46280858, top_logprobs={" of": -0.46280858}),
                    Token(text=" the", logprob=-1.4058315, top_logprobs={" the": -1.4058315}),
                    Token(text=" foundations", logprob=-2.0638132, top_logprobs={" foundations": -2.0638132}),
                    Token(text=" of", logprob=-0.2607486, top_logprobs={" of": -0.2607486}),
                    Token(text=" artificial", logprob=-1.1653417, top_logprobs={" artificial": -1.1653417}),
                    Token(text=" intelligence", logprob=-0.03756146, top_logprobs={" intelligence": -0.03756146}),
                    Token(text=" (", logprob=-2.019812, top_logprobs={",": -1.3503861}),
                    Token(text="AI", logprob=-0.03869382, top_logprobs={"AI": -0.03869382}),
                    Token(text=")", logprob=-0.49895737, top_logprobs={")": -0.49895737}),
                    Token(text=" and", logprob=-0.81909865, top_logprobs={" and": -0.81909865}),
                    Token(text=" related", logprob=-2.611718, top_logprobs={" to": -2.3555496}),
                    Token(text=" fields", logprob=-0.7640527, top_logprobs={" fields": -0.7640527}),
                    Token(text=".", logprob=-1.8066244, top_logprobs={",": -1.2972366}),
                    Token(text=" It", logprob=-2.2856107, top_logprobs={"\n": -1.7865871}),
                    Token(text=" focuses", logprob=-3.3735154, top_logprobs={" is": -1.4982711}),
                    Token(text=" on", logprob=-0.13244776, top_logprobs={" on": -0.13244776}),
                    Token(text=" foundational", logprob=-1.2640914, top_logprobs={" foundational": -1.2640914}),
                    Token(text=" questions", logprob=-2.010647, top_logprobs={" issues": -1.673752}),
                    Token(text=" in", logprob=-1.980726, top_logprobs={" that": -1.8133409}),
                    Token(text=" AI", logprob=-0.5709368, top_logprobs={" AI": -0.5709368}),
                    Token(text=",", logprob=-1.036094, top_logprobs={",": -1.036094}),
                    Token(text=" which", logprob=-3.826836, top_logprobs={" such": -2.0843854}),
                    Token(text=" are", logprob=-1.3858839, top_logprobs={" are": -1.3858839}),
                ],
            )
        ]

        # Verified against https://beta.openai.com/tokenizer. Prompt + completions = 51 + 32.
        assert self.token_counter.count_tokens(request, completions) == 51 + 32

    def test_estimate_tokens(self):
        request = Request(prompt=TestOpenAITokenCounter.TEST_PROMPT, num_completions=3, max_tokens=100)

        # Prompt + max number of tokens from completions = 51 + 3 * 100
        assert self.token_counter.estimate_tokens(request) == 51 + 3 * 100

    def test_fits_within_context_window(self):
        # Should fit in the context window since we subtracted the number of tokens of the test prompt
        # from the max context window
        assert self.token_counter.fits_within_context_window(TestOpenAITokenCounter.TEST_PROMPT, 2049 - 51)
        # Should not fit in the context window because we're expecting one more extra token in the completion
        assert not self.token_counter.fits_within_context_window(TestOpenAITokenCounter.TEST_PROMPT, 2049 - 51 + 1)

    def test_truncate(self):
        # Create a prompt that exceed max context length: 51 * 41 = 2091 tokens
        long_prompt: str = TestOpenAITokenCounter.TEST_PROMPT * 41
        assert not self.token_counter.fits_within_context_window(long_prompt)

        # Truncate and ensure it fits within the context window
        truncated_long_prompt: str = self.token_counter.truncate(long_prompt)
        assert self.token_counter.fits_within_context_window(truncated_long_prompt)
