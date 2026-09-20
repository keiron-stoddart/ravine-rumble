"""John Hecht's weekly Ravine Rumble power rankings, transcribed from the Google Doc.

To add a week: append one entry ({"week": N, "rank": R, "writeup": "..."}) to every
team's "entries" list. An entry may also carry a "tagline" (the headline after the
team name) and a "team" (only when the team was named differently that week). The page
derives the weeks, movement, and highlights from this data.
"""

from declarations import SEASON_2026_POWER_RANKINGS_URL

POWER_RANKINGS = {
    "author": "John Hecht",
    "source_url": SEASON_2026_POWER_RANKINGS_URL,
    "teams": [
        {
            "manager": "Brett",
            "team": "Wonsuperbowl",
            "color": "#1d6fb8",
            "entries": [
                {
                    "week": 1,
                    "rank": 1,
                    "tagline": "Repeat?",
                    "writeup": "After finally claiming a title, this team gets to kickoff the year with the clear number one player in the league in Gibbs. Brett’s second pick in Jeanty was a fringe first rounder a month ago before an ankle injury and fell all the way to 24. Follow that up with a Devonta Smith ready to get the JSN treatment and you’ve got a strong foundation. Layer on Tuten who fills the Etienne spot on a Jaguars offense that got it going last year, Caleb who in his second year with Ben Johnson is ready to put it all together, and DK Metcalf in the 9th could be a top 24 WR in the best offense the Steelers have had in 9 years. Add Jayden Reed, Brooks, Allgeier, last year’s MVP Stafford as a backup, and the monster leg of Cam Little, it’s hard to see this team not making a run at a title.",
                },
                {
                    "week": 2,
                    "rank": 1,
                    "writeup": "Gibbs and Caleb look like an MVP combination and Brett also found a Jeanty between the couch cushions with the 24th pick. Depth be damned. Sure, his wide receivers (bench included) combined for a total 11 receptions. I don’t care. Gibbs and Jeanty look electric.",
                },
            ],
        },
        {
            "manager": "Brian",
            "team": "Covfefe Crew",
            "color": "#d35400",
            "entries": [
                {
                    "week": 1,
                    "rank": 2,
                    "tagline": "I’d trade for this team",
                    "writeup": "This team is all gas and they just need a match. This team will have the most highlight plays all season long. Bijan, Pickens, Bowers, and Jamo are all 99.999% football freaks who would look like aliens if they travelled back in time to play a game in the 90s. Depth is the only issue here with TreVeyon already dinged up, but this team has options to address that during the season. One thing to watch out for is the Falcons packing it in mid-season to lock in a top draft pick. Snagging BJT, Lawrence, Corum, and a jilted Mahomes in the middle rounds might make this a super team right out of the gate.",
                },
                {
                    "week": 2,
                    "rank": 7,
                    "writeup": "Sunday was over on Friday for this team. I said this team is “all gas” but there was not a single spark to get it going. Bijan’s performance was uninspiring, Pickens dropped a TD bomb, Burden gooned while the rest of the Bears went nuclear, and Bowers decided to get a casual meniscus trim 3 days before the start of the season.",
                },
            ],
        },
        {
            "manager": "John",
            "team": "Big Green Machine",
            "color": "#1e8449",
            "entries": [
                {
                    "week": 1,
                    "rank": 3,
                    "tagline": "Ricky Bobby",
                    "writeup": "If CMC plays, you win. If he’s hurt, you lose. Well, John is tired of losing so taking CMC over JTT, Amon-Ra, and others was an easy choice. An identity crisis appears to be at stake this season. Countless hours spent thinking about offensive coordinators, schedules, splits, when to take a kicker, what teams to fade have all led to this. Previous versions of John would’ve puked at the idea of taking a kicker in the 10th, laughed at the idea of co-siging the Patriots, and rolled their eyes at taking Javonte for the 4th time in his five seasons, but this is it. There is no honor in being good. You have to win. I must win.",
                },
                {
                    "week": 2,
                    "rank": 9,
                    "writeup": "10 minutes into the season and John was already spiraling. Unable to even enjoy the misery of Patriots fans, John immediately regretted tying his joy to the success of a team he hates, a player he didn’t trust, and a coach who looks like he “wants to getaway”. John needs a new hobby.",
                },
            ],
        },
        {
            "manager": "Tyler",
            "team": "BirdsArentReal",
            "color": "#c0392b",
            "entries": [
                {
                    "week": 1,
                    "rank": 4,
                    "tagline": "What could go wrong?",
                    "writeup": "After trying to get the draft moved the morning of, Birds found a way to get it done. The Chase/Burrow stack is the fajitas of the fantasy football world. It comes out sizzling from the kitchen and it gets the attention of everyone in the restaurant leaving the rest of the room questioning their life decisions. But here’s the secret about fajitas, they often disappoint. Everyone who has tried the Bengals experience leaves wanting more and this year could be no different as the Bengals did little to fix their offensive line. Add in the a Range Rover that is Drake London, looks good on the lot but is going to break down within 3 months, Quinshon Judkins who is coming off an injury, Lloyd who has played 4 games and you have a rickety roster. Kyren is as safe an investment there is in the league giving Tyler a good floor, but any Bengals hiccup is going to send Tyler into the a tailspin.",
                },
                {
                    "week": 2,
                    "rank": 12,
                    "writeup": "I called this team fajitas. Nothing sizzles quite Joe Burrow and Chase coming out of the tunnel, but boy did they fizzle. How many picks would Tyler like to do over again? 1? 2? 10? Pray for a bounceback.",
                },
            ],
        },
        {
            "manager": "Pat",
            "team": "Ebron James",
            "color": "#7d3c98",
            "entries": [
                {
                    "week": 1,
                    "rank": 5,
                    "tagline": "Hall of Fame call went to his head",
                    "writeup": "Pat decided he wanted to juggle swords all season with his first pick of Puka, who had an off-season more inline with a Breaking Bad character than All-Pro WR. Nico is the number one WR for a QB who showed up to training camp looking like Doug Funny, Olave is one head bonk away from taking a sabbatical, Love is already hurt and on a team whose fans want nothing more than to lose every single game this season. Add Lamar who is the only player to show up on injury reports each year with a common cold, the enigma that is Kyle Pitts who has no QB, and Alec Pierce who had an ankle surgery after signing a ridiculous deal for catching 3 fewer passes than Jerry Jeudy and you have team of living on the edge. This team could score 200 points one week and 80 the next. The one saving grace is that the Rams decided to spend 24 hours in Australia and Puka will be supervised the entire time. Any longer and he’d probably die by kangaroo.",
                },
                {
                    "week": 2,
                    "rank": 3,
                    "writeup": "Puka going to Australia and leaving alive is a win. I don’t care about the points, he’s going to be a monster. Add in Nico and bobblehead Olave and that is the best WR trio in the league. And, Lamar looked so back. Imagine being that athletic and transcendent and being stuck under the tutelage of a washed Uncle like Harbaugh. This is now Lamar’s team and he’s going to remind everyone what he can do.",
                },
            ],
        },
        {
            "manager": "Dan",
            "team": "Plaxidantal Discharge",
            "color": "#6e4b3a",
            "entries": [
                {
                    "week": 1,
                    "rank": 6,
                    "tagline": "Team least likely to read or care about these rankings",
                    "writeup": "Not hard to see that this draft is likely on a third screen for Dan. He always scoops up the players people leave behind. Amon-Ra, who is still the leader on a fading Lions team, Chase Brown, in the running for most anonymous player in the first 5 rounds of drafts, and Rashee Rice, who spent a month in jail this summer, make up a foundation that no one would be excited to watch each Sunday. But that doesn’t matter for the mystery man who may have 3 fantasy leagues or 100. We’ll never know. Add in change of scenery RBs in Etienne and Montgomery and players fans are just done with in Pollard, Pittman, and Andrews, this team will churn out points but never look like a juggernaut.",
                },
                {
                    "week": 2,
                    "rank": 4,
                    "writeup": "Dan picks up all the dollar bills we leave behind and ends up turning a profit every single damn year. Amon-Ra is as boring a stock there is but is going to beat the market every time. Add in Montgomery, Brown, and Rice, this team looks more like a law firm than a roster of surefire dogs.",
                },
            ],
        },
        {
            "manager": "Zach",
            "team": "Allen’s Army",
            "color": "#c2185b",
            "entries": [
                {
                    "week": 1,
                    "rank": 7,
                    "tagline": "Setting himself up for heartbreak",
                    "writeup": "If players didn’t get hurt, this team would be in for a nice Sunday drive. Unfortunately, football requires large humans to smash slightly smaller humans making this team one injury away from panic drive. Walker miraculously stayed healthy for an all-time Super Bowl run and his reward for such a team achievement? The Seahawks saying, “We’re good,” and he gets to go to a Chiefs team who haven’t had a meaningful rusher in 6 years. Zach put all his fantasy chips and fan chips in the DJ Moore basket and needs him to be a top 10 guy if he’s going to put together a complete team. RB Depth is going to prove difficult with Monongai already dinged up and Woody Marks being usurped. Everyone wants the Bills to be good, but Zach is person who needs them to be.",
                },
                {
                    "week": 2,
                    "rank": 2,
                    "writeup": "When will we learn there is no bad time to draft Josh Allen. He’s dependable, incredible, and inevitable. You draft Allen and you get a free pass to the playoffs. Add in a Ken Walker who looked even better than he did during his playoff run last year and you don’t care that Lamb didn’t do much.",
                },
            ],
        },
        {
            "manager": "Tim",
            "team": "Booty Meat",
            "color": "#3f51b5",
            "entries": [
                {
                    "week": 1,
                    "rank": 8,
                    "tagline": "We can tell the Browns hurt him",
                    "writeup": "No Browns in the first five rounds and only four on the roster? Either the Browns hurt Tim or he’s gearing up for a run. Saquon and Achane could be RB1/2, Waddle could finally excel no longer shackled to Tua, and both Marvin and Egbuka are going to be peppered with targets all year long. Everyone was scared off of Fannin and Tim may be rewarded for listening to his heart. Chances are Tim knows only 50% of these players but vibes are high for this team. The worry here is that Achane is going to be on a bad bad bad bad bad bad team. Fortunately for Tim, he’s used to supporting bad bad bad bad bad bad teams.",
                },
                {
                    "week": 2,
                    "rank": 11,
                    "writeup": "All time regret team? Banking on the Eagles, the Dolphins, Waddle, Browns, and Marvin Harrison Jr? Eagles looked the same as last year, Waddle had one catch, Browns gave up after the first quarter, and Harrison is the team’s 18th option. Tim would trade this whole squad in a minute if he could.",
                },
            ],
        },
        {
            "manager": "Nan",
            "team": "Green Bay Parsons",
            "color": "#0e7c86",
            "entries": [
                {
                    "week": 1,
                    "rank": 9,
                    "team": "ProstiTUTEN",
                    "tagline": "Can’t believe this team believes in Danny Dimes",
                    "writeup": "Of all the managers in the league I thought would fall for the Danny Dime Colts, Nan was at the bottom of the list. Jonathan Taylor is a great football player but I’m not trusting a team who decided to go all in after 6 weeks of fools gold. The Colts have a better chance of being a bottom 5 team than a contender and that won’t matter because their pick belongs to the Jets now. No one enjoys suffering more than Nan so I’m sure he’ll handle the Danny Dimes experience with grace. Derrick Henry is the Mountain and will always be in December and January but this team has to get to the playoffs for that to matter. This team could come alive in the second half with Kraft getting up to speed, Tate and Lemon getting their legs, and Murray proving everybody wrong. But I bet right now, Nan would trade JTT and Flowers for Saquon and Ladd if he had to do it over again.",
                },
                {
                    "week": 2,
                    "rank": 6,
                    "writeup": "Derrick Henry doing that in September is terrifying. I cannot fathom trying to tackle that man. He had players making business decisions in week 1. This team is dinged because Zay went down, but as long as King Henry gets the rock they have a chance.",
                },
            ],
        },
        {
            "manager": "Paul",
            "team": "Daddy Dart",
            "color": "#8a7d00",
            "entries": [
                {
                    "week": 1,
                    "rank": 10,
                    "tagline": "Going back to the autodraft well",
                    "writeup": "Justin Jefferson at 20? McBride at 29? Hurts, a guaranteed 10 rushing TDs, in the 5th? That looks like a homerun. The back half? Not so much. Josh Downs, Aaron Jones, Xavier Worthy, Deebo, Both Steelers RBs are all players most wouldn’t take if they had an extra roster spot. Paul’s been here before and has a title to back it up, but I don’t see a Ja’Marr Chase hiding on his roster anywhere. Paul finds a way to get into the narrative so something will go his way. Just not sure what that is yet.",
                },
                {
                    "week": 2,
                    "rank": 5,
                    "writeup": "Besmirch autodraft at your own risk. Paul is doing it right. Put in the least amount of effort and exact the most amount of pleasure. What could go wrong? JSN, JJ, and McBride are going to float this boat all year long.",
                },
            ],
        },
        {
            "manager": "Keiron",
            "team": "Brady’s Bunch",
            "color": "#ad1457",
            "entries": [
                {
                    "week": 1,
                    "rank": 11,
                    "tagline": "Pulled hammies incoming",
                    "writeup": "When was the last time the Chargers stayed healthy? Anyone? Can anyone remember a time when the LA Chargers, the remora fish to the sharks that are the Rams, gave anyone confidence they could “put it all together”? Since 2021, Herbert has been sacked 193 times, behind only Geno and Baker, 12 times more than Burrow, and 72 more times than Tua. Everyone is in love with the idea of the Chargers but when has the idea of something ever lived up to the reality? Higgins, Watson, and Evans all have timeshares on the IR and often like to extend their stays. I like James Cook, but this team is one pulled hammy away from tilting into oblivion.",
                },
                {
                    "week": 2,
                    "rank": 10,
                    "writeup": "How many Chargers is too many Chargers? After week 1, the answer seems to be 1. The bones of this team are solid, but they may have to play whack-a-mole every week trying to figure out which oft-injured receivers and tight ends to play.",
                },
            ],
        },
        {
            "manager": "Wonjoon",
            "team": "Wonjoon",
            "color": "#558b2f",
            "entries": [
                {
                    "week": 1,
                    "rank": 12,
                    "tagline": "More Blue Tent visits than wins",
                    "writeup": "Committed to the bit, this team is loaded with New York’s finest (Skattebo & Wilson) and its dregs (AD Mitchell & Geno). It may be humorous from a distance, but up close this team is going to worry its weekly opponents. Nabers, Breece, and Wilson at one point in their careers have all been fantasy darlings targeted in the first two rounds of drafts. Dart, when not in the blue tent, is a top 5 fantasy QB. Skattebo, whose foot did a 180 10 months ago, is doing flips because he is a psycho. This isn’t a team that can string together 17 weeks, but that was never the plan. This team is going to ruin someone’s season and that is all Wonjoon ever wanted.",
                },
                {
                    "week": 2,
                    "rank": 8,
                    "writeup": "Jets and Giants both started 1-0 for the first time since 2009. People will credit Harbaugh joining the Giants or Geno having a bit left in the tank for the Jets. But 2009 was also the inaugural year of the Ravine Rumble. Coincidence? Wonjoon raising his effort 5% may have reversed the fortunes of 3 long suffering franchises.",
                },
            ],
        },
    ],
}
