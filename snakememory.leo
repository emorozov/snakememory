<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="35" clone_windows="0"/>
<globals body_outline_ratio="0.473333333333">
	<global_window_position top="0" left="0" height="850" width="780"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences>
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="eugene.20041109114950" a="E"><vh>Algorithms</vh>
<v t="eugene.20041027174727.1"><vh>SuperMemo Learning Algorithm, ver. 2.0</vh>
<v t="eugene.20041112121402"><vh>Step 1</vh></v>
<v t="eugene.20041112121402.1"><vh>Step 2</vh></v>
<v t="eugene.20041112121402.2"><vh>Step 3</vh></v>
<v t="eugene.20041112121402.3"><vh>Step 4</vh></v>
<v t="eugene.20041112121402.4"><vh>Step 5</vh></v>
<v t="eugene.20041112121402.5"><vh>Step 6</vh></v>
<v t="eugene.20041112121402.6"><vh>Step 7</vh></v>
</v>
<v t="eugene.20041102121618"><vh>SuperMemo Algorithm, ver. 11</vh></v>
</v>
<v t="eugene.20041027174727" a="E"><vh>TODO</vh>
<v t="eugene.20041129004015"><vh>Debug drill problem</vh></v>
<v t="eugene.20041128134818"><vh>Copy, cut, paste card</vh></v>
<v t="eugene.20041111162229.1" a="E"><vh>Support for multimedia questions and answers</vh>
<v t="eugene.20041121002003"><vh>Support for replacing sounds</vh></v>
<v t="eugene.20041120233207"><vh>Option for selecting audio player</vh></v>
</v>
<v t="eugene.20041127010503"><vh>Plugins for chinese/japanese characters</vh></v>
<v t="eugene.20041127094244"><vh>New items should be added as siblings</vh></v>
<v t="eugene.20041125110743" a="E"><vh>Support for drawing answers</vh>
<v t="eugene.20041125173917"><vh>Clear, color buttons</vh></v>
<v t="eugene.20041125173917.1"><vh>Draw lines between points?</vh></v>
</v>
<v t="eugene.20041121145010"><vh>Clean and crossplatform installation</vh></v>
<v t="eugene.20041121003527" a="E"><vh>Split and clean SnakeStore</vh></v>
<v t="eugene.20041111162429"><vh>Unit tests for everything</vh></v>
<v t="eugene.20041127233604"><vh>Some structured storage for xml and media files</vh></v>
<v t="eugene.20041125173840" a="E"><vh>Gnome goals are incompatible with Win32</vh>
<v t="eugene.20041125110743.1"><vh>Panel applet</vh></v>
</v>
<v t="eugene.20041116200139.1" a="E"><vh>Port to Win32</vh></v>
<v t="eugene.20041116205714" a="E"><vh>Toolkit independence</vh>
<v t="eugene.20041116205846"><vh>Fetch widgets in views</vh></v>
</v>
<v t="eugene.20041113012427"><vh>Item metadata?</vh></v>
<v t="eugene.20041109114950.1"><vh>schedule recalculation every day</vh></v>
<v t="eugene.20041111155240"><vh>closing recall window must be equal to selecting null quality</vh></v>
<v t="eugene.20041110151141"><vh>Implement namespaces support for importing HTML</vh></v>
<v t="eugene.20041112163320"><vh>Port to Windows CE</vh></v>
</v>
<v t="eugene.20041109165356" a="E"><vh>BUGS</vh>
<v t="eugene.20041109165334"><vh>rescheduled item is not saved</vh></v>
<v t="eugene.20041124200107"><vh>gtk doesn't support mng files</vh></v>
</v>
<v t="eugene.20041025180618" a="E"><vh>PyFlashcard</vh>
<v t="eugene.20041103145917" a="E"
expanded="eugene.20041106214235,eugene.20041103170106,eugene.20041124210449,eugene.20041103164710,eugene.20041112164453,eugene.20041103164135,eugene.20041121125204,eugene.20041121130713,eugene.20041121143923,eugene.20041125154525,eugene.20041125154525.1,eugene.20041125154525.2,eugene.20041110135237,eugene.20041110135237.1,eugene.20041110135237.4,eugene.20041109125829,eugene.20041109125829.1,eugene.20041109131225,eugene.20041103171145,eugene.20041103172037,eugene.20041103171145.1,eugene.20041113122546,eugene.20041113123359,eugene.20041113123359.3,eugene.20041103171033,eugene.20041103155300,eugene.20041103153955,"><vh>@thin snakememory.py</vh></v>
<v t="eugene.20041029161735"
expanded="eugene.20041029161735.2,"><vh>@thin xmlwriter.py</vh></v>
</v>
<v t="eugene.20041116201512"><vh>Installation script</vh>
<v t="eugene.20041116201512.1" a="E"><vh>@thin install.py</vh></v>
</v>
<v t="eugene.20041108135942" a="E"><vh>Unit tests</vh>
<v t="eugene.20041108144653" a="E"><vh>@thin tests/testall.py</vh></v>
<v t="eugene.20041108152153" a="E"
expanded="eugene.20041108152444,"><vh>@thin tests/testSnakeStore.py</vh></v>
<v t="eugene.20041108135942.1" a="E"
expanded="eugene.20041108141556,"><vh>@thin tests/testItem.py</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="eugene.20041025180618"></t>
<t tx="eugene.20041027174727"></t>
<t tx="eugene.20041027174727.1">@
I wrote the first SuperMemo program in December 1987 (Turbo Pascal 3.0, IBM PC). It was intended to enhance the SuperMemo method in two basic ways:

   1. apply the optimization procedures to smallest possible items (in the paper-based SuperMemo items were grouped in pages),
   2. differentiate between the items on the base of their different difficulty.

Having observed that subsequent inter-repetition intervals are increasing by an approximately constant factor (e.g. two in the case of the SM-0 algorithm for English vocabulary), I decided to apply the following formula to calculate inter-repetition intervals:

    I(1):=1
    I(2):=6
    for n&gt;2 I(n):=I(n-1)*EF

where:

    I(n) - inter-repetition interval after the n-th repetition (in days)
    EF - easiness factor reflecting the easiness of memorizing and retaining a given item in memory (later called the E-Factor).

E-Factors were allowed to vary between 1.1 for the most difficult items and 2.5 for the easiest ones. At the moment of introducing an item into a SuperMemo database, its E-Factor was assumed to equal 2.5. In the course of repetitions this value was gradually decreased in case of recall problems. Thus the greater problems an item caused in recall, the more significant was the decrease of its E-Factor.

Shortly after the first SuperMemo program had been implemented, I noticed that E-Factors should not fall below the value of 1.3. Items having E-Factors lower than 1.3 were repeated annoyingly often and always seemed to have inherent flaws in their formulation (usually they did not conform to the minimum information principle). Thus not letting E-Factors fall below 1.3 substantially improved the throughput of the process and provided an indicator of items that should be reformulated. The formula used in calculating new E-Factors for items was constructed heuristically and did not change much in the following 3.5 years of using the computer-based SuperMemo method.

In order to calculate the new value of an E-Factor, the student has to assess the quality of his response to the question asked during the repetition of an item (my SuperMemo programs use the 0-5 grade scale - the range determined by the ergonomics of using the numeric key-pad). The general form of the formula used was:

    EF':=f(EF,q)

where:

    EF' - new value of the E-Factor
    EF - old value of the E-Factor
    q - quality of the response
    f - function used in calculating EF'.

The function f had initially multiplicative character and was in later versions of SuperMemo program, when the interpretation of E-Factors changed substantially, converted into an additive one without significant alteration of dependencies between EF', EF and q. To simplify further considerations only the function f in its latest shape is taken into account:

    EF':=EF-0.8+0.28*q-0.02*q*q

which is a reduced form of:

    EF':=EF+(0.1-(5-q)*(0.08+(5-q)*0.02))

Note, that for q=4 the E-Factor does not change.

Let us now consider the final form of the SM-2 algorithm that with minor changes was used in the SuperMemo programs, versions 1.0-3.0 between December 13, 1987 and March 9, 1989 (the name SM-2 was chosen because of the fact that SuperMemo 2.0 was by far the most popular version implementing this algorithm).

Algorithm SM-2 used in the computer-based variant of the SuperMemo method and involving the calculation of easiness factors for particular items:

@others

The optimization procedure used in finding E-Factors proved to be very effective. In SuperMemo programs you will always find an option for displaying the distribution of E-Factors (later called the E-Distribution). The shape of the E-Distribution in a given database was roughly established within few months since the outset of repetitions. This means that E-Factors did not change significantly after that period and it is safe to presume that E-Factors correspond roughly to the real factor by which the inter-repetition intervals should increase in successive repetitions.

During the first year of using the SM-2 algorithm (learning English vocabulary), I memorized 10,255 items. The time required for creating the database and for repetitions amounted to 41 minutes per day. This corresponds to the acquisition rate of 270 items/year/min. The overall retention was 89.3%, but after excluding the recently memorized items (intervals below 3 weeks) which do not exhibit properly determined E-Factors the retention amounted to 92%. Comparing the SM-0 and SM-2 algorithms one must consider the fact that in the former case the retention was artificially high because of hints the student is given while repeating items of a given page. Items preceding the one in question can easily suggest the correct answer.
Therefore the SM-2 algorithm, though not stunning in terms of quantitative comparisons, marked the second major improvement of the SuperMemo method after the introduction of the concept of optimal intervals back in 1985. Separating items previously grouped in pages and introducing E-Factors were the two major components of the improved algorithm. Constructed by means of the trial-and-error approach, the SM-2 algorithm proved in practice the correctness of nearly all basic assumptions that led to its conception.</t>
<t tx="eugene.20041102121618">@nocolor
Algorithm SM-11

SuperMemo computes optimum inter-repetition interval by storing the recall record of individual items. This record is used to estimate the current strength of a given memory trace, and the difficulty of the underlying piece of knowledge (item). The item difficulty expresses the complexity of memories, and reflects the effort needed to produce unambiguous and stable memory traces. SuperMemo takes the requested recall rate as the optimization criterion (e.g. 95%), and computes the intervals that satisfy this criterion. The function of optimum intervals is represented in a matrix form (OF matrix) and is subject to modification based on the results of the learning process.

Important! Algorithm SM-11 is used only to compute the intervals between repetitions of items. Topics are reviewed at intervals computed with an entirely different algorithm (not described here).

This is a more detailed description of the Algorithm SM-11:

   1. Optimum interval: Inter-repetition intervals are computed using the following formula:

          I(1)=OF[1,L+1]
          I(n)=I(n-1)*OF[n,AF]

      where:

              * OF - matrix of optimal factors, which is modified in the course of repetitions
              * OF[1,L+1] - value of the OF matrix entry taken from the first row and the L+1 column
              * OF[n,AF] - value of the OF matrix entry that corresponds with the n-th repetition, and with item difficulty AF
              * L - number of times a given item has been forgotten (from "memory Lapses")
              * AF - number that reflects absolute difficulty of a given item (from "Absolute difficulty Factor")
              * I(n) - n-th inter-repetition interval for a givent item 

   2. Advanced repetitions: Because of possible advancement in executing repetitions (e.g. forced review before an exam), the actual optimum factor (OF) used to compute the optimum interval is decremented by dOF using formulas that account for the spacing effect in learning:

          dOF=dOFmax*a/(thalf+a)
          dOFmax=(OF-1)*(OI+thalf-1)/(OI-1)

      where:

              * dOF - decrement to OF resulting from the spacing effect
              * a - advancement of the repetition in days as compared with the optimum schedule (note that there is no change to OF if a=0, i.e. the repetition takes time at optimum time)
              * dOFmax - asymptotic limit on dOF for infinite a (note that for a=OI-1 the decrement will be OF-1 which corresponds to no increase in inter-repetition interval)
              * thalf - advancement at which there is half the expected increase to synaptic strength as a result of a repetition (presently this value corresponds roughly to 60% of the length of the optimum interval for well-structured material)
              * OF - optimum factor (i.e. OF[n,AF] for the n-th interval and a given value of AF)
              * OI - optimum interval (as derived from the matrix OF)

   3. Delayed repetitions: Because of possible delays in executing repetitions, matrix OF is not actually indexed with repetitions but with repetition categories. For example if the 5-th repetition is delayed, OF matrix is used to compute the repetition category, i.e. the theoretical value of the repetition number that corresponds with the interval used before the repetition. The repetition category may, for example, assume the value 5.3 and we will arrive at I(5)=I(4)*OF[5.3,AF] where OF[5.3,AF] has a intermediate value derived from OF[5,AF] and OF[6,AF] 
   4. Matrix of optimum intervals: SuperMemo does not store the matrix of optimum intervals as in some earlier versions. Instead it keeps a matrix of optimal factors that can be converted to the matrix of optimum intervals (as in the formula from Point 1). The matrix of optimal factors OF used in Point 1 has been derived from the mathematical model of forgetting and from similar matrices built on data collected in years of repetitions in collections created by a number of users. Its initial setting corresponds with values found for a less-than-average student. During repetitions, upon collecting more and more data about the student’s memory, the matrix is gradually modified to make it approach closely the actual student’s memory properties. After years of repetitions, new data can be fed back to generate more accurate initial matrix OF. In SuperMemo 2002, this matrix can be viewed in 3D with Tools : Statistics : Analysis : 3-D Graphs : O-Factor Matrix
   5. Item difficulty: The absolute item difficulty factor (A-Factor), denoted AF in Point 1, expresses the difficulty of an item (the higher it is, the easier the item). It is worth noting that AF=OF[2,AF]. In other words, AF denotes the optimum interval increase factor after the second repetition. This is also equivalent with the highest interval increase factor for a given item. Unlike E-Factors in Algorithm SM-6 employed in SuperMemo 6 and SuperMemo 7, A-Factors express absolute item difficulty and do not depend on the difficulty of other items in the same collection of study material (see FAQs for explanation)
   6. Deriving OF matrix from RF matrix: Optimum values of the entries of the OF matrix are derived through a sequence of approximation procedures from the RF matrix which is defined in the same way as the OF matrix (see Point 1), with the exception that its values are taken from the real learning process of the student for who the optimization is run. Initially, matrices OF and RF are identical; however, entries of the RF matrix are modified with each repetition, and a new value of the OF matrix is computed from the RF matrix by using approximation procedures. This effectively produces the OF matrix as a smoothed up form of the RF matrix. In simple terms, the RF matrix at any given moment corresponds to its best-fit value derived from the learning process; however, each entry is considered a best-fit entry on it’s own, i.e. in abstraction from the values of other RF entries. At the same time, the OF matrix is considered a best-fit as a whole. In other words, the RF matrix is computed entry by entry during repetitions, while the OF matrix is a smoothed copy of the RF matrix
   7. Forgetting curves: Individual entries of the RF matrix are computed from forgetting curves approximated for each entry individually. Each forgetting curve corresponds with a different value of the repetition number and a different value of A-Factor (or memory lapses in the case of the first repetition). The value of the RF matrix entry corresponds to the moment in time where the forgetting curve passes the knowledge retention point derived from the requested forgetting index. For example, for the first repetition of a new item, if the forgetting index equals 10%, and after four days the knowledge retention indicated by the forgetting curve drops below 90% value, the value of RF[1,1] is taken as four. This means that all items entering the learning process will be repeated after four days (assuming that the matrices OF and RF do not differ at the first row of the first column). This satisfies the main premise of SuperMemo, that the repetition should take place at the moment when the forgetting probability equals 100% minus the forgetting index stated as percentage. In SuperMemo 2002, forgetting curves can be viewed with Tools : Statistics : Analysis : Curves (or in 3-D with Tools : Statistics : Analysis : 3-D Curves):
   8. Deriving OF matrix from the forgetting curves: The OF matrix is derived from the RF matrix by: (1) fixed-point power approximation of the R-Factor decline along the RF matrix columns (the fixed point corresponds to second repetition at which the approximation curve passes through the A-Factor value), (2) for all columns, computing D-Factor which expresses the decay constant of the power approximation, (3) linear regression of D-Factor change across the RF matrix columns and (4) deriving the entire OF matrix from the slope and intercept of the straight line that makes up the best fit in the D-Factor graph. The exact formulas used in this final step go beyond the scope of this illustration.
      Note that the first row of the OF matrix is computed in a different way. It corresponds to the best-fit exponential curve obtained from the first row of the RF matrix.
      All the above steps are passed after each repetition. In other words, the theoretically optimum value of the OF matrix is updated as soon as new forgetting curve data is collected, i.e. at the moment, during the repetition, when the student, by providing a grade, states the correct recall or wrong recall (i.e. forgetting) (in Algorithm SM-6, a separate procedure Approximate had to be used to find the best-fit OF matrix, and the OF matrix used at repetitions might differ substantially from its best-fit value)
   9. Item difficulty: The initial value of A-Factor is derived from the first grade obtained by the item, and the correlation graph of the first grade and A-Factor (G-AF graph). This graph is updated after each repetition in which a new A-Factor value is estimated and correlated with the item’s first grade. Subsequent approximations of the real A-Factor value are done after each repetition by using grades, OF matrix, and a correlation graph that shows the correspondence of the grade with the expected forgetting index (FI-G graph). The grade used to compute the initial A-Factor is normalized, i.e. adjusted for the difference between the actually used interval and the optimum interval for the forgetting index equal 10%
  10. Grades vs. the expected forgetting index correlation: The FI-G graph is updated after each repetition by using the expected forgetting index and grade values. The expected forgetting index can easily be derived from the interval used between repetitions and the optimum interval computed from the OF matrix. The higher the value of the expected forgetting index, the lower the grade. From the grade and the FI-G graph (see FI-G graph in Analysis), we can compute the estimated forgetting index which corresponds to the post-repetition estimation of the forgetting probability of the just-repeated item at the hypothetical pre-repetition stage. Because of the stochastic nature of forgetting and recall, the same item might or might not be recalled depending on the current overall cognitive status of the brain; even if the strength and retrievability of memories of all contributing synapses is/was identical! This way we can speak about the pre-repetition recall probability of an item that has just been recalled (or not). This probability is expressed by the estimated forgetting index
  11. Computing A-Factors: From (1) the estimated forgetting index, (2) length of the interval and (3) the OF matrix, we can easily compute the most accurate value of A-Factor. Note that A-Factor serves as an index to the OF matrix, while the estimated forgetting index allows one to find the column of the OF matrix for which the optimum interval corresponds with the actually used interval corrected for the deviation of the estimated forgetting index from the requested forgetting index

To sum it up. Repetitions result in computing a set of parameters characterizing the memory of the student: RF matrix, G-AF graph, and FI-G graph. They are also used to compute A-Factors of individual items that characterize the difficulty of the learned material. The RF matrix is smoothed up to produce the OF matrix, which in turn is used in computing the optimum inter-repetition interval for items of different difficulty (A-Factor) and different number of repetitions (or memory lapses in the case of the first repetition). Initially, all student’s memory parameters are taken as for a less-than-average student, while all A-Factors are assumed to be equal.

Optimization solutions used in Algorithm SM-11 have been perfected over 15 years of using the SuperMemo method with computer-based algorithms (first implementation: December 1987). This makes sure that the convergence of the starting memory parameters with the actual parameters of the student proceeds in a very short time. In addition, Algorithm SM-11 includes mechanisms that make it insensitive to interference from the deviation from the optimum repetition timing (e.g. delayed or advanced repetitions). The introduction of A-Factors and the use of the G-AF graph greatly enhanced the speed of estimating item difficulty. The adopted solutions are the result of constant research into new algorithmic variants. The postulated employment of neural networks in repetition spacing is not likely to compete with the presented algebraic solution. 

Algorithm SM-11 is constantly being perfected in successive releases of SuperMemo, esp. to account for newly collected repetition data, convergence data, input parameters, etc.

</t>
<t tx="eugene.20041108135942"></t>
<t tx="eugene.20041109114950"></t>
<t tx="eugene.20041109114950.1"></t>
<t tx="eugene.20041109165334">@
If there's only one event during session: rescheduling of the item that wasn't repeated on schedule, items are not saved on disk. I.e. rescheduling will continue endlessly until some other event won't trigger SnakeStore.save()

This is a very unlikely event, but probably need to be fixed anyway.
</t>
<t tx="eugene.20041109165356"></t>
<t tx="eugene.20041110151141"></t>
<t tx="eugene.20041111155240"></t>
<t tx="eugene.20041111162229.1"></t>
<t tx="eugene.20041111162429"></t>
<t tx="eugene.20041112121402">@
1. Split the knowledge into smallest possible items.
</t>
<t tx="eugene.20041112121402.1">@
2. With all items associate an E-Factor equal to 2.5.
</t>
<t tx="eugene.20041112121402.2">@
3. Repeat items using the following intervals:
   I(1):=1
   I(2):=6
   for n&gt;2: I(n):=I(n-1)*EF
   where:
     I(n) - inter-repetition interval after the n-th repetition (in days),
     EF - E-Factor of a given item
     If interval is a fraction, round it up to the nearest integer.
</t>
<t tx="eugene.20041112121402.3">@
4. After each repetition assess the quality of repetition response in 0-5 grade scale:
   5 - perfect response
   4 - correct response after a hesitation
   3 - correct response recalled with serious difficulty
   2 - incorrect response; where the correct one seemed easy to recall
   1 - incorrect response; the correct one remembered
   0 - complete blackout.
</t>
<t tx="eugene.20041112121402.4">@
5. After each repetition modify the E-Factor of the recently repeated item according to the formula:
   EF':=EF+(0.1-(5-q)*(0.08+(5-q)*0.02))
   where:
   EF' - new value of the E-Factor,
   EF - old value of the E-Factor,
   q - quality of the response in the 0-5 grade scale.
If EF is less than 1.3 then let EF be 1.3.
</t>
<t tx="eugene.20041112121402.5">@
6. If the quality response was lower than 3 then start repetitions for the item from the beginning without changing the E-Factor (i.e. use intervals I(1), I(2) etc. as if the item was memorized anew).
</t>
<t tx="eugene.20041112121402.6">@
7. After each repetition session of a given day repeat again all items that scored below four in the quality assessment. Continue the repetitions until all of these items score at least four.
</t>
<t tx="eugene.20041112163320"></t>
<t tx="eugene.20041113012427"></t>
<t tx="eugene.20041116200139.1"></t>
<t tx="eugene.20041116201512"></t>
<t tx="eugene.20041116205714"></t>
<t tx="eugene.20041116205846"></t>
<t tx="eugene.20041120233207"></t>
<t tx="eugene.20041121002003"></t>
<t tx="eugene.20041121003527"></t>
<t tx="eugene.20041121145010"></t>
<t tx="eugene.20041124200107"></t>
<t tx="eugene.20041125110743"></t>
<t tx="eugene.20041125110743.1"></t>
<t tx="eugene.20041125173840"></t>
<t tx="eugene.20041125173917"></t>
<t tx="eugene.20041125173917.1"></t>
<t tx="eugene.20041127010503"></t>
<t tx="eugene.20041127094244"></t>
<t tx="eugene.20041127233604"></t>
<t tx="eugene.20041128134818"></t>
<t tx="eugene.20041129004015"></t>
</tnodes>
</leo_file>
