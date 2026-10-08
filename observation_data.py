from observation import Observation

possible_observations = {
    "Sunrise": [
        Observation(
            "\nAmy reading",
            "Amy",
            "Local library",
            """\nAmy picks a book off the nonfiction section.
You catch a glimpse of the cover.
'An understanding of the human mind.'
A phsycology book."""
        )
    ],

    "Morning": [
        Observation(
            "\nAmy writing",
            "Amy",
            "Classroom 11A",
            """\nAmy quietly writes in her notebook.
The page is full of detailed observations about her classmates.
\nShe ocassionaly glances at Emma's empty seat next to her.
It's been left untouched ever since she went missing.""",
reveals_student="Amy"
        ),
        
        Observation(
            "\nDistracted Mia",
            "Mia",
            "Classroom 11B",
            """Mia is anxiously fiddling with her pen.
She doesn't make any effort to pay attention to the class.
Her emotions are unstable."""
        ),
    ],

    "Noon": [
        Observation(
        "\nZoe arguing with students.",
        "Zoe",
        "Cafeteria",
        """Zoe argues with 3 other students.
She throws her can of soda into their faces.
That gets them to back off."""),

        Observation(
        "\nEthan nervously eating Doritos",
        "Ethan",
        "Cafeteria",
        """Ethan sits with a bag of Doritos.
The bag is nearly finished, but he somehow keeps finding more.
\nHe keeps checking his phone, like he's waiting for something."""),
    
        Observation(
            "\nMia is anxious.",
            "Mia",
            "Hallway",
            """Mia talks with her small circle of friends in the hallway.
Mia pretends she's indifferent towards Emma..
But she always adjusts her cyan headband when she's mentioned."""
        ),
        ],

    "Afternoon": [
        Observation(
            "\nZoe fixing",
            "Zoe",
            "Classroom 11D",
            """Zoe seems focused on her backpack.
She's fixing a small tear in it.
Her hands are rough with calluses."""
        ),

        Observation(
            "\nAmy receiving a note",
            "Amy",
            "Classroom 11A",
            """Amy is focused on her test sheet, patiently working on each answer.
A student tries to pass her a note.
They're trying to copy her work.
Amy doesn't spare them a glance before tossing it into the bin."""
        )

    ],

    "Night": [

    ]
}