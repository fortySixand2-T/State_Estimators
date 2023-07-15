load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_library(
    name = "datatypes",
    hdrs = ["covariance_structs.h",
            "motion_model_states.h",
            "state.h"],
    deps = [
        "@eigen",
    ],
    visibility = ['//visibility:public']
)