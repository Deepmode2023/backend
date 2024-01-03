POST_SPACED_REPETITION = {"name": "CreateRepetition", "description": "You create a repetition with a string `description`. But you can use slang and pass `description` with slang tags to manipulate the output more flexibly.You can learn more at www.deepmode.pl/api-docs/slang or https://github.com/Deepmode2023/backend.",
                          "success": "You have successfully updated the repeat date"}
DELETE_SPACED_REPETITION = {"name": "DeleteRepetition", "description": "",
                            "success": "You have successfully deleted the repetition"}


GET_SPACED_REPETITION = {"name": "GetSpacedRepetition", "description": "In this item you will get all your repeats that are bound to your account. Mandatory fields `date_start`, `date_end` - return repeats in this deapozone. If you pass `slug` , `title` - it will sort first by date and then filter by `slug` or `title` from the selected repeats.",
                         "success": "You have successfully obtained a list of your reps!"}
