load("//bzl:module.bzl", "isaac_subgraph")
load("//bzl:py.bzl", "isaac_py_app")

isaac_subgraph(
    name = "object_detection_subgraph",
    data = [
        "@industrial_dolly_pose_estimation_cnn_model",
    ],
    modules = [
        "detect_net",
        "ml",
        "perception"
    ],
    subgraph = "graphs/subgraphs/object_detection.subgraph.json",
    visibility = ["//visibility:public"],
)

isaac_subgraph(
    name = "edge_detection_subgraph",
    subgraph = "graphs/subgraphs/edge_detection.subgraph.json",
    visibility = ["//visibility:public"],
)

isaac_py_app(
    name = "object_detection",
    srcs = glob(["codelets/*"]) + ["main.py"],
    main = "main.py",
    data = [
        "object_detection_subgraph",
        "edge_detection_subgraph",
        "graphs/detection.app.json",
        "//packages/navsim/apps:navsim_training_subgraph",
    ],
    modules = [
        "sight",
        "viewers",
    ],
    deps = [
        "//packages/pyalice",
    ],
)

