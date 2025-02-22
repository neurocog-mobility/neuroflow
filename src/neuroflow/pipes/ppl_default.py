from kedro.pipeline import Pipeline, node, pipeline

from neuroflow.nodes.template_node import node_template


def ppl_default(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=node_template,
                inputs="parameters",
                outputs="",
                name="template_node",
            ),
        ]
    )
