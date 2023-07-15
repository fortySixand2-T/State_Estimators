load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_library(
    name = "motion_models",
    hdrs = ["motion_models.h",
            "constant_acceleration_model.h"],
    deps = [
        "@eigen", "//datatypes:datatypes",
    ],
    visibility = ['//visibility:public']
)