from catwalk.task import MC_METRICS, InstanceFormat, ENTAILMENT_METRICS
from catwalk.tasks.eleuther import EleutherPerplexityTask, EleutherHFTask
from catwalk.tasks.huggingface import hfmc_conversion, HFDatasetsTask
from catwalk.tasks.t5 import t5_prompt_conversion

TASKS = {
    "wikitext": EleutherPerplexityTask("wikitext"),
    "piqa": EleutherHFTask("piqa").add_instance_conversion(
        InstanceFormat.HF_MC,
        hfmc_conversion(
            context_field=None,
            question_field="goal",
            answer_choices_fields=["sol1", "sol2"],
            correct_answer_index_field="label"
        )
    ).add_metrics(MC_METRICS),
    "squad2": EleutherHFTask("squad2"),
    "glue::rte": EleutherHFTask("rte").add_instance_conversion(
        InstanceFormat.T5_PROMPT,
        t5_prompt_conversion(
            task_name="rte",
            label_map={0: "entailment", 1: "not_entailment"},
            use_fields=["sentence1", "sentence2"]
        )
    ).add_metrics(ENTAILMENT_METRICS),
    "superglue::rte": HFDatasetsTask("super_glue", "rte").add_instance_conversion(
        InstanceFormat.T5_PROMPT,
        t5_prompt_conversion(
            task_name="rte",
            label_map={0: "entailment", 1: "not_entailment"},
            use_fields=["premise", "hypothesis"]
        )
    ).add_metrics(ENTAILMENT_METRICS),
}
