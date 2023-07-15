load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_library(
    name = "filter",
    hdrs = ["include/filter.h"],
    deps = [
        "@eigen",
    ],
)
cc_binary(
    name = "filters",
    srcs = ["include/filter.cpp", "main.cpp"],
    deps = [":filter"]
    # deps = ["@com_google_absl//absl/strings","/usr/share/libeigen3-dev"]
)