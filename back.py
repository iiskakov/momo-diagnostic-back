import ell
from typing import List
from pydantic import BaseModel
from ell import Message
from utils.openai_client import get_openrouter_client

openrouter_client, extra_body = get_openrouter_client()



@ell.simple(model="anthropic/claude-3.7-sonnet", max_tokens=5000, client=openrouter_client, extra_body=extra_body)
def analyze_assessment(assessment_data):
    return f"""Your task is to provide a short analysis of a kid's math topics assessment. It will be given to a parent, so be empathetic, warm, but truthful. Highlight the strong sides, and also say a bit about areas that could be improved. You've done thousands of such and you're truly a mastermind of finding interesting patterns and talking to parents. Here is raw data {assessment_data}"""

@ell.complex(model="anthropic/claude-3.7-sonnet", max_tokens=5000, client=openrouter_client, extra_body=extra_body)
def assess_math_skills(message_history: List[Message]) -> List[Message]:
    return [
        ell.system("""Here are the topics to explore in this session:
    Operations on Numbers
    Thinking Algebraically
    Place Value
    Comparing Whole Numbers
    Adding Whole Numbers
    Subtracting Whole Numbers
    Factors, Products, and Multiples
    Multiplying Whole Numbers
    Multiplying Whole Numbers Using Models
    Dividing Whole Numbers
    Dividing Whole Numbers Using Models
    Fractions
    Mixed Numbers
    Comparing Fractions
    Adding Fractions
    Adding Mixed Numbers
    Multiplying Fractions
    Decimals
    Units
    Representing and Interpreting Data
    Geometry


                   Your task is to simulate an adaptive math diagnostic through parent-child interaction that identifies the child's "knowledge frontier" - the boundary between what they know and don't know in mathematics.

During this diagnostic session:
1. Ask questions that provide maximum information gain about multiple related topics simultaneously
2. Adapt your questioning path based on previous answers to efficiently map knowledge boundaries
3. Consider both accuracy AND solution time when assessing mastery
4. Start with broad classification questions and progressively narrow to specific areas
5. Balance maintaining the child's engagement with diagnostic efficiency

Question selection strategy:
- Begin with engaging, moderate-confidence questions to build rapport
- Each response should provide evidence about the tested skill AND its prerequisites/postrequisites
- Prioritize questions at the estimated "frontier" of the child's knowledge
- If a child answers a question correctly but slowly, treat this as partial evidence of mastery
- When a child struggles, explore prerequisite topics to identify foundational gaps

When assessing mastery:
- Consider speed of response alongside correctness
- Look for patterns that suggest conceptual understanding versus mechanical application
- Note if the child shows anxiety or confidence with particular topic areas
- Use incorrect answers diagnostically to identify specific misconceptions

Topics to examine remain the same as in your original list.

Maintain the Russian language requirement, one instruction-one reply format, A/B/C answer structure, and the specified JSON response format as originally outlined.

For the final summary, briefly identify the child's knowledge frontier - highlighting both strengths and areas where foundations may need strengthening, while keeping it warm and supportive.

    For each topic/skill mastery we will also have a confidence of a prediction. If some of them have low confidence it's okay to ask additional questions to increase out confidence. 
    Always use russian language. For the final summary, keep it short, warm and empathetic, if there are interesting data points or patterns tell parent about them, but don't create recommendations.



Strategic Question Sequencing 
If it helps the situation - chain questions in specific sequences so each response provides multiple data points. For example:

Q1: "Did they solve it in under 30 seconds?"
- A tells us: speed + likely mastery
- B tells us: methodical worker
- C tells us: possible difficulty level

Q2 (if previous was A): "Did they explain their solution?"
- A tells us: true understanding + communication
- B tells us: mechanical mastery only
- C tells us: possible lucky guess on first question

Embedded Assessment Codes
We can embed emotional/behavioral assessment into math questions:

"Present this addition problem. BEFORE they solve it, select:
A: They started immediately
B: They took a moment but looked confident
C: They showed hesitation or anxiety"



    Reply in a JSON format, that has.
    1. Instruction for a parent to follow
    2. Possible answers 
    3. Current data we have collected. Only add skills that were tested. Start with confidence level not too high.
    4. How complete the diagnostic is, in percent (starts with 0)
    5. Final summary (only fill in when after the assessment is complete). keep empty otherwise

NEVER use code blocks like ```json ```
ALWAYS use this raw json schema in your replies:
                   {
  "type": "object",
  "properties": {
    "assessment_completion": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "instruction": { "type": "string" },
    "possible_answers": {
      "type": "object",
      "properties": {
        "a": { "type": "string" },
        "b": { "type": "string" },
        "c": { "type": "string" }
      },
      "required": ["a", "b", "c"]
    },
    "collected_data": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "mastery": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": ["mastery", "confidence"]
      }
    },
    "final_summary": { "type": "string" }
  },
  "required": ["instruction", "possible_answers", "collected_data", "assessment_completion", "final_summary"]
} """),
    
    ] + message_history


@ell.simple(model="anthropic/claude-3.7-sonnet:thinking", max_tokens=5000, client=openrouter_client, extra_body=extra_body)
def create_learning_path(diagnostic_results):
    # Use double curly braces for literal curly braces in the f-string
    # And concatenate the diagnostic_results as a separate string instead of embedding it in the f-string
    template = f"""<math_topic_dependency_tree>
graph TD
    %% --- Node Definitions ---
    AncientMath[Ancient Mathematics];
    ArithProp[Arithmetic Properties];
    Base10[Base 10 Place Value];
    Base5[Base 5];
    Base2[Base 2];
    AddDeep[Addition: Deep Dive];
    MultDeep[Multiplication: Deep Dive];
    NegSub[Negative Numbers & Subtraction];
    Division[Division];
    RoundEstComp[Rounding, Estimation, Comparison];
    IntroFrac[Introduction to Fractions];
    FracDeep[Fractions: Deep Dive];
    Decimals[Decimals];
    EvenOdd[Even & Odd Numbers];
    PrimeComp[Prime & Composite Numbers];
    Fibonacci[Fibonacci-Virahanka Numbers];
    EarlyGeom[Early Geometry];
    EarlyProb[Early Probability Theory];
    BasicCount[Basic Counting & Number Recognition];

    %% --- Subgraphs for Logical Grouping (Optional Styling) ---
    subgraph S0 [Level 0: Context & Foundational Concepts]
        direction LR
        AncientMath;
        BasicCount;
        EvenOdd;
    end

    subgraph S1 [Level 1: Core Base 10 & Addition]
        direction LR
        Base10;
        ArithProp;
        AddDeep;
        RoundEstComp;
    end

    subgraph S2 [Level 2: Multiplication, Subtraction & Early Applications]
        direction LR
        MultDeep;
        NegSub;
        Fibonacci;
        EarlyGeom;
    end

    subgraph S3 [Level 3: Division & Factoring]
        direction LR
        Division;
        PrimeComp;
    end

    subgraph S4 [Level 4: Rational Numbers & Other Bases]
        direction TB
        IntroFrac;
        FracDeep;
        Decimals;
        Base5;
        Base2;
    end

    subgraph S5 [Level 5: Probability]
        EarlyProb;
    end

    %% --- Dependencies (Prerequisite --> Topic) ---

    %% Foundational Links
    AncientMath --> BasicCount;
    BasicCount --> Base10;
    BasicCount --> EvenOdd;
    BasicCount --> EarlyGeom;

    %% Core Arithmetic Links
    Base10 --> AddDeep;
    Base10 --> RoundEstComp;
    Base10 --> ArithProp;
    Base10 --> Decimals;
    Base10 --> Base5;
    Base10 --> Base2;

    ArithProp --> AddDeep;
    ArithProp --> MultDeep;

    AddDeep --> MultDeep;
    AddDeep --> NegSub;
    AddDeep --> Fibonacci;
    AddDeep --> EarlyGeom;

    %% Intermediate Operations & Concepts Links
    MultDeep --> Division;
    MultDeep --> PrimeComp;
    MultDeep --> FracDeep;

    NegSub --> Division;
    NegSub --> FracDeep;

    Division --> IntroFrac;
    Division --> PrimeComp;
    Division --> Decimals;
    Division --> FracDeep;

    %% Rational Numbers & Applications Links
    IntroFrac --> FracDeep;
    IntroFrac --> Decimals;
    IntroFrac --> EarlyProb;

    %% Fractions Deep Dive requires all basic operations
    AddDeep --> FracDeep;

    %% Decimals also require basic operations (implicitly via Base10 path)
    AddDeep --> Decimals;
    NegSub --> Decimals;
    MultDeep --> Decimals;
    Division --> Decimals;

    %% --- Styling (Optional: makes arrows clearer) ---
    linkStyle default interpolate basis

</math_topic_dependency_tree>

<diagnostic_results>
"""

    # Add the diagnostic results as plain string concatenation
    template += str(diagnostic_results)
    
    # Continue with the rest of the template using double curly braces for literal curly braces
    template += """
</diagnostic_results>


Goal: Create an efficient and effective learning sequence tailored to the individual student.

Steps:

    Map the Diagnosis: Take the diagnostic results and mark each topic on your Knowledge Map accordingly (e.g., Green=Known, Yellow=Weak/Conditionally Known, Red=Unknown).

    Identify the Knowledge Frontier: Look for the "boundary" topics. These are typically the Red (Unknown) topics whose direct prerequisites are Green (Known) or maybe Yellow (Weak). These are the topics the student is structurally ready to learn next.

    Prioritize Foundational Gaps:

        Identify any Red or Yellow topics that are prerequisites for many other topics, especially those needed for the student's main goal (e.g., their current course level).

        These foundational gaps often need attention before or alongside more advanced topics.

    Select Initial Learning Targets: Choose 1-3 topics from the Knowledge Frontier to start with. Consider:

        Prerequisites Met: Only pick topics where immediate prerequisites are Green or maybe Yellow (if you plan to reinforce the Yellow ones quickly).

        Foundational Needs: If critical foundations are missing for the student's main goal, prioritize learning those foundations once they reach the point they are blocked.

        Student Motivation (The Course Goal): If possible, include topics from the student's current course level that don't depend on missing foundations to build momentum and engagement early on.

        Avoid Interference: Try to select topics from different branches of the map if learning multiple things simultaneously, rather than very similar concepts (e.g., don't teach adding fractions and multiplying fractions on the exact same day initially).

    Learn & Assess: Have the student work on the selected target topic(s). Focus on reaching mastery (understanding and fluency).

    Update the Map: Once a topic is mastered, change its status on your map (e.g., from Red/Yellow to Green).

    Monitor & Adapt:

        If the student struggles unexpectedly with a target topic, check their understanding of its prerequisites (even Green ones). You might need to loop back for review ("Fall Backwards").

        If a Yellow (Weak) topic seems shaky when used as a prerequisite, plan specific practice/review for it.

    Repeat: Go back to Step 2 (Identify the new Knowledge Frontier) and continue selecting the next appropriate topics based on the updated map. Incorporate spaced review of previously learned (Green) topics periodically.

Key Principle: Always respect the prerequisite links on the map. Don't try to teach a topic if its foundations aren't solid. Use the map to guide the order and the diagnostic results to know the starting point and weak spots. Be flexible and adjust based on how the student actually performs.

Your reply must ALWAYS have a confing string. It should ALWAYS be wrapped in <config_string></config_string> XML tags. (No braces)
Here is the string format needed:

Skill Tree Encoding System - Simplified Explanation
Our skill tree encoding uses a compact string format to define the entire structure of learning paths:
5l
Key Components:
Node Definition: Each node is written as a number + letter
Number: Represents the game's unique short ID (not array position)
Letter: Indicates initial state
c = Completed/Available
l = Locked
Connections:
> shows a prerequisite relationship: left node unlocks right node(s)
, separates multiple target nodes
Segments: Separated by ; to define different relationships
Example Decoded:
1c>2l,3c;2l>4c;3c>5l means:
Game ID 1 starts available, and unlocks games 2 (locked) and 3 (available)
Game ID 2 (locked until 1 is completed) unlocks game 4
Game ID 3 (available) unlocks game 5 (locked)

And here are the game mappings:

{ id: 'gen3', name: 'Addition Basic', numId: 2 },
    { id: 'gen5', name: 'Fractions Intro', numId: 3 },
    { id: 'gen7', name: 'Multiplication Basic', numId: 4 },
    { id: 'gen8', name: 'Geometry', numId: 5 },
    { id: 'gen9', name: 'Ancient math', numId: 6 },
    { id: 'gen10', name: 'Place Value', numId: 7 },
    { id: 'gen11', name: 'Multiplication', numId: 8 },
    { id: 'gen12', name: 'Division Basic', numId: 9 },
    { id: 'gen13', name: 'Subtraction Basic', numId: 10 },
    { id: 'gen14', name: 'Units', numId: 11 },
    { id: 'gen15', name: 'Decimals', numId: 12 },
    { id: 'gen20', name: 'Comparing Fractions', numId: 13 },
    { id: 'gen21', name: 'Prime Numbers', numId: 14 },
    { id: 'gen22', name: 'Commutative Property', numId: 15 },


    """
    
    return template
