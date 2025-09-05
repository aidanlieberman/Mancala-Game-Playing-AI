Intro: Mancala is an ancient board game, dating back at least 5000 years. Now, CS students are
tasked with writing artificial intelligence programs to mastermind this game. During the past
week and a half, team AlPHA (Aidan lieberman, Philip, Hailey, Alex) constructed an algorithm to
win at Mancala every time. But how did they do it? Read on!
<img width="688" height="284" alt="Screenshot 2025-09-05 at 5 28 42 PM" src="https://github.com/user-attachments/assets/cce82e06-2a09-4daa-b43b-a742d123ada2" /> 

^Game Tree Visualized, from Stanford Algorithms Course 

1. Our program had a 100% win rate against a random opponent when tested on a sample of
100 games. We also played against the program ourselves, and were able to win a game
against it. However, we did know which heuristic the program was using which may have
allowed us to gain an advantage against it.

2. From the initial board state, the algorithm can reach a search depth of 8 in 0.4 seconds while
a search depth of 9 exceeds one second. This was tested on a laptop with 16GB of RAM and
an Intel Ultra 7 155H processor with a clock speed of 3.8 GHz. The use of alpha-beta pruning
significantly improved performance, reducing the time to reach a search depth of 8 from 9.2
seconds to 0.4 seconds. However, when performing the alpha-beta pruning we did not attempt
to order the moves by checking the most promising ones first. This could have improved the
performance of the alpha-beta pruning algorithm further and potentially let us search to a
greater depth, but it did not end up being necessary.

3. We chose to use a relatively simple heuristic, namely calculating the difference between the
number of stones in our mancala and the number of stones in the opponent’s mancala. This
heuristic allowed us to win all games against random, minimax, and alphabeta as listed on
gradescope. We considered modifying the heuristic to take into account various potential
captures or whose side the stones are on, but ultimately a simple heuristic that was quick to
calculate combined with an adequate search depth allowed us to win every game.

Aidan Lieberman (alieber6@u.rochester.edu)
Alex Novak (anovak5@u.rochester.edu)
Philip Hollett (phollett@u.rochester.edu)
Hailey Wong-Budiman (hwongbud@u.rochester.edu)
