Adaptive Multisensory Learning Platform for Dyslexic Children Using Real-time AI-Powered Content Personalization
A PROJECT REVIEW REPORT 2

Submitted by
PRATHAPAN S (412722205031)
DEEPAK SR (412722205006)
ROHITH K (412722205037)
DHINESH MP (412722205010)

in partial fulfilment for the award of the degree
of
BACHELOR OF TECHNOLOGY
in
INFORMATION TECHNOLOGY

[COLLEGE NAME]
[COLLEGE ADDRESS]
[UNIVERSITY NAME]
[MONTH YEAR]


ABSTRACT
Adaptive Multisensory Learning Platform is an AI-powered educational system designed to improve reading, spelling, and comprehension for dyslexic children through real-time personalization. Dyslexia is often under-diagnosed and many children are detected only after repeated school failure. Inspired by the IEEE Access base paper "Screening Dyslexia Using Visual Auditory Computer Games and Machine Learning" (2025), our project uses short, language-independent visual and auditory computer games to collect interaction measures that can distinguish learners with different difficulty patterns. The proposed platform integrates multisensory instruction (visual and auditory), interactive game-based learning, and continuous learning analytics to tailor content dynamically. It monitors learner performance indicators such as accuracy, response time, retry count, error pattern distribution, and sensory success rate. An offline-trained AI layer supports decision-making: a tree-based classifier (aligned with the base paper’s Extra Trees / boosting approach) identifies the learner struggle type (Normal, Phonics issue, Spelling issue, Visual issue), an MLP regression model forecasts future performance using recent session trends, and a DQN reinforcement learning agent learns the optimal teaching strategy by selecting the best difficulty and sensory mode combination. During deployment, the system continuously follows a loop of Play -> Analyze -> Predict -> Decide -> Adapt, updating game parameters after each round and providing real-time insights to parents and teachers via a progress dashboard. By combining evidence-based visual+auditory screening games with adaptive AI-driven personalization, the platform aims to increase engagement, detect struggle areas early, and improve literacy outcomes in an inclusive, scalable learning environment.


LITERATURE SURVEY
2.1 TITLE: Screening Dyslexia Using Visual Auditory Computer Games and Machine Learning
AUTHOR: Maria Rauschenberger, Ricardo Baeza-Yates, Luz Rello
YEAR: 2025
Description:
This IEEE Access paper presents a language-independent approach for screening dyslexia using visual and auditory computer games combined with machine learning. The authors designed a short game (less than 15 minutes) with 16 stages (each stage has 2 rounds) following a Whac-A-Mole style interaction: (i) a visual search task where children remember a target cue and then click targets among distractors (2x2 and 3x3 grids), and (ii) an auditory working-memory task where children remember a target sound cue and then identify it among distractors. Data were collected from 137 children (51 with dyslexia) across different languages (German, Spanish, English). The paper trains non-linear classifiers (Random Forest, Extra Trees, Gradient Boosting) using 10-fold cross-validation and reports results such as precision/recall around 0.78/0.79 for German and 0.83/0.80 for all languages using Extra Trees. The work motivates our project’s core design choice: using visual + auditory game-derived measures for low-cost screening and then extending this pipeline into real-time personalization.

2.2 TITLE: Predicting Risk of Dyslexia With an Online Gamified Test
AUTHOR: Luz Rello, Ricardo Baeza-Yates, A. Ali, J. P. Bigham, M. Serra
YEAR: 2020
Description:
This work studies dyslexia risk prediction using an online gamified test and shows that interaction-based measures collected from games can be used for screening. The authors design short web games, log response times, accuracy and interaction patterns, and then train machine learning models to classify children into risk vs. control groups, demonstrating that purely behavioral HCI features can achieve useful screening performance at scale. Their study highlights practical aspects such as browser/device diversity, imbalanced data, and the importance of choosing robust metrics (e.g., F1-score, balanced accuracy) when evaluating screening tools. It supports the feasibility of online, inexpensive, game-based data collection without specialized hardware or long clinical tests, and shows that meaningful predictions can be obtained from relatively short sessions. In our project, we adopt the same idea of game telemetry and extend it with multisensory (visual+auditory) tasks and a live personalization layer (difficulty and sensory mode adaptation), so that the same telemetry used for screening is also reused to drive teaching decisions and long-term progress monitoring.

2.3 TITLE: Serious Games for Early Identification of Developmental Dyslexia
AUTHOR: O. Gaggi, C. E. Palazzi, M. Ciman, G. Galiazzo, S. Franceschini, M. Ruffino, S. Gori, A. Facoetti
YEAR: 2017
Description:
This paper supports the use of serious games for early identification and screening of developmental dyslexia. The authors design game-based tasks that operationalize known dyslexia indicators and show that children’s performance inside the game (scores, errors, timing) can be used to distinguish risk groups, making screening more engaging than traditional tests. The study emphasizes that diagnostic sensitivity can be preserved while replacing traditional test-like interfaces with playful environments, provided that game mechanics are carefully aligned with cognitive constructs. It reinforces that game-based interactions can capture meaningful signals related to dyslexia indicators and that carefully chosen mechanics (rewards, time limits, progressive difficulty) help maintain motivation during assessment and reduce test anxiety. This motivates our choice of using engaging serious-game mechanics for assessment and continuous data collection before and during adaptive training sessions in our platform, ensuring that our screening and personalization pipeline remains child-friendly while still grounded in established dyslexia indicators.


SYSTEM ANALYSIS
3.1 EXISTING SYSTEM
Existing dyslexia support and detection methods rely heavily on linguistic assessments (reading/spelling tests) and manual observation in classrooms. Dyslexia is often under-diagnosed, and many children are identified only after repeated failure at school. Traditional support methods (classroom teaching, worksheets, and many educational apps) use fixed learning paths and a teacher-controlled pace. They do not continuously analyze interaction measures from learning tasks, and they rarely adapt the sensory modality (visual vs. auditory) or difficulty level in real time. As a result, learners may experience repeated errors, low motivation, and reduced confidence, and targeted intervention becomes slow and dependent on specialist availability.
Disadvantages
- Uniform pace for all learners.
- No real-time content adaptation.
- Limited learner behavior analytics.
- Lower engagement and motivation.
- High dependency on teachers for personalization.

3.2 PROPOSED SYSTEM
The proposed system is an AI-driven adaptive multisensory learning platform built on the same core idea as the 2025 IEEE Access base paper: using short, language-independent visual and auditory games to collect screening measures. Following the base paper’s game design principles, our platform includes (1) a visual search task with targets and distractors (2x2 and 3x3 style grids) and (2) an auditory working-memory task where the learner remembers a target sound cue and identifies it among distractors. From these game rounds, the system logs interaction measures and aggregates them into features such as accuracy, response time, retry count, error pattern distribution, and sensory success rate.

We extend the base paper from binary screening into a live personalization pipeline. After each mini-session, a tree-based classifier (e.g., XGBoost, consistent with the base paper’s tree ensemble results) estimates the struggle type (Normal / Phonics / Spelling / Visual). After a session window, an MLP regression model forecasts near-future performance and risk using recent trends. After each round, a DQN reinforcement learning agent selects the next learning action (difficulty + sensory mode) to maximize improvement. A parent/teacher dashboard provides continuous visibility into current level, struggle classification, predicted improvement, risk score, and session trend graphs, supporting inclusive education and reducing manual workload.
Advantages
- Personalized learning experience for each child.
- Early detection of struggle areas (phonics/spelling/visual).
- Automatic difficulty and sensory mode adaptation.
- Higher engagement through multisensory game-based learning.
- Real-time progress monitoring for parents and teachers.

3.3 SYSTEM ARCHITECTURE
User Interaction
       |
Game Engine
       |
Data Logger
       |
AI Layer
   |-- XGBoost -> Struggle Type
   |-- MLP -> Performance Prediction
   `-- DQN -> Adaptive Decision
       |
Updated Game Parameters
       |
User Plays Adapted Content
       |
Dashboard Update

3.4 MODULES
1. User Authentication & Session Initialization
2. Screening Games (Visual + Auditory) & Data Logger
3. Feature Engineering & Screening Classifier (Tree Ensemble)
4. Personalization Engine (MLP Forecast + DQN Policy)
5. Dashboard & Reporting


1. User Authentication & Session Initialization
This module manages student login and securely initializes a learning session by loading prior learning history and profile settings. It prepares the session timeline and baseline metrics for the first mini-assessment. Role-based access ensures students access games while parents/teachers access the dashboard. In a full deployment, this module also supports privacy controls for child data and ensures only authorized stakeholders can view performance analytics.

2. Screening Games (Visual + Auditory) & Data Logger
This module implements the language-independent screening tasks aligned with the base paper. The visual game uses a search-task interaction where the learner first sees (primes) a target cue and then must locate/click it among distractors within a time limit, with difficulty increased by denser grids (e.g., 2x2 then 3x3). The auditory game targets auditory working memory: the learner listens to a target sound cue and then identifies it among distractors, with options to replay cues. The Data Logger records fine-grained telemetry per round (correct/incorrect, time, retries, and error patterns) and aggregates them into session-level features for the screening and personalization models.

3. Feature Engineering & Screening Classifier (Tree Ensemble)
This module transforms raw game telemetry into a stable feature vector. Inspired by the base paper’s successful use of tree ensembles (Extra Trees / Random Forest / Gradient Boosting), we use a tree-based classifier (e.g., XGBoost) to estimate the learner’s difficulty profile. Unlike the base paper which focuses on binary screening (dyslexia risk vs. control), our project extends classification into actionable struggle categories (Normal / Phonics / Spelling / Visual) to support personalization decisions.

4. Personalization Engine (MLP Forecast + DQN Policy)
This module predicts and optimizes learning outcomes during deployment. The MLP regression model forecasts near-future accuracy and risk using recent trends (e.g., last 5–10 rounds/sessions). The DQN reinforcement learning agent then selects the next instructional action from combinations of difficulty (Easy/Medium/Hard) and sensory mode (Visual/Audio). The reward function is based on improvement in accuracy, reduction in retries, and reduction in response time, enabling the system to learn a policy that adapts to each learner’s needs over time.

5. Dashboard & Reporting
This module provides a real-time dashboard for parents and teachers. It displays the current difficulty level, identified struggle classification, predicted improvement percentage, risk score, and session trend graphs. The dashboard updates continuously as the student plays and as the AI layer produces new outputs, supporting timely intervention and progress tracking. In extended versions, this module can generate periodic reports per week/month and provide recommendations for home practice aligned with detected struggle areas.
