TASKS = {

    "python_basics": {

        "title":"Python Basics",

        "required_concepts":[
            "variable",
            "loop",
            "function",
            "data type",
            "condition"
        ]
    },

    "oops": {

        "title":"Object Oriented Programming",

        "required_concepts":[
            "class",
            "object",
            "inheritance",
            "polymorphism",
            "encapsulation"
        ]
    }
}


def get_task(task_id):

    return TASKS.get(task_id)