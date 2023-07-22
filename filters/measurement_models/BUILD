load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_library(
    name = "measurement_models",
    hdrs = ["position_measurement.h",
            ],
    deps = [
        "@eigen", "//datatypes:datatypes",
    ],
    visibility = ['//visibility:public']
)