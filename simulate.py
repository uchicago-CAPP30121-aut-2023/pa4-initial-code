"""
Polling places

YOUR NAME(s) HERE

Main file for polling place simulation
"""

import random
import queue
import click
import util



### YOUR Voter class GOES HERE.


class VotingBooths:
    """
    Class for representing a bank of voting booths.

    Attributes
    ----------
    None

    Methods
    -------
    is_booth_available(): boolean
        is there at least one unoccupied booth
    is_some_booth_occupied(): boolean
        is there at least one occupied booth
    enter_booth(v): 
        add a voter to a booth. requires a booth to be available.
    time_next_free(): float
        when will a booth be free next (only called when all the
        booths are occupied)
    exit_booth():
        remove the next voter to depart from the booths and
        return the voter and their departure_time.
    """

    def __init__(self, num_booths):
        """
        Initialize the voting booths.

        Args:
            num_booths: (int) the number of voting booths in the bank
        """

        self._num_booths = num_booths
        self._q = queue.PriorityQueue()

    def is_booth_available(self):
        """Is at least one booth open"""
        return self._q.qsize() < self._num_booths

    def is_some_booth_occupied(self):
        """Is at least one booth occupied"""
        return self._q.qsize() > 0

    def enter_booth(self, v):
        """
        Add voter v to an open booth

        Args:
            v: (Voter) the voter to add to the booth.

        Requirements: there must be an open booth.
        """
        assert self.is_booth_available(), "All booths in use"
        assert v.start_time, "Voter's start time must be set."

        dt = v.start_time + v.voting_duration
        self._q.put((dt, v))

    def time_next_free(self):
        """
        When will the next voter leave?

        Returns: next departure time

        Requirements: there must be at least one occupied booth.
        """
        assert self.is_some_booth_occupied(), "No booths in use"

        # PriorityQueue does not have a peek method.
        # So, do a get followed by a put.
        (dt, v) = self._q.get()
        self._q.put((dt, v))
        return dt


    def exit_booth(self):
        """
        Remove voter with lowest departure time.

        Returns: the voter and the voter's departure time

        Requirements: there must be at least one occupied booth.
        """
        assert self.is_some_booth_occupied(), "No booths in use"

        (dt, v) = self._q.get()
        return v, dt


class Precinct:
    """
    Class for representing precincts.

    Attributes
    ----------
    None

    Methods
    -------
    simulate(seed, voting_booths, impatience_threshold):
        Simulate election day for the precinct using the
        specified seed, voting_booths, and impatience threshold.
    """

    def __init__(self, name, hours_open, num_voters, arrival_rate,
                 voting_duration_rate, impatience_prob):
        """
        Constructor for the Precinct class

        Args:
            name: (str) Name of the precinct
            hours_open: (int) Hours the precinct will remain open
            num_voters: (int) Number of voters in the precinct
            arrival_rate: (float) Rate at which voters arrive
            voting_duration_rate: (float) Lambda for voting duration
            impatience_prob: (float) the probability that a voter
                will be impatient.
        """

        # YOUR CODE HERE

        # REPLACE "pass" with your constructor implementation
        pass


    def simulate(self, seed, voting_booths, impatience_threshold):
        """
        Simulate election day for the precinct using the specified seed,
        voting_booths, and impatience threshold.

        Args:
            seed: (int) the seed for the random number generator
            voting_booths: (VotingBooths) the voting booths assigned to the
                precinct for the day
            impatience_threshold: (int) the number of minutes an impatient voter
                is willing to wait (inclusive)

        Returns: (list of Voter) the list of Voters
        """

        # YOUR CODE HERE

        # REPLACE [] with appropriate return value
        return []


def find_impatience_threshold(seed, precinct, num_booths, num_trials):
    """
    For a given precinct, find the impatience threshold at which all
    voters are likely to vote.

    Args:
        seed (int): the initial seed for the random number generator
        precinct: (Precinct) the precinct to simulate
        num_booths: (int) number of voting booths to use in
            the simulations
        num_trials: (int) the number of trials to run

    Returns: (int) the median threshold from the trials
    """

    assert num_trials > 0

    # YOUR CODE HERE

    # Replace None with a suitable return value
    return None


def find_voting_booths_needed(seed, precinct, imp_threshold, num_trials):
    """
    For a given precinct, seed, and impatience threshold, predict the number of
    booths needed to make it likely that all the voters will vote.

    Args:
        seed (int): the initial seed for the random number generator
        precinct: (Precinct) the precinct to simulate
        impatience_threshold: (int) the impatience threshold
        num_trials: (int) the number of trials to run

    Returns: (int) the median number of booths needed from the trials.
    """

    assert num_trials > 0

    # YOUR CODE HERE

    # Replace None with a suitable return value
    return None


@click.command(name="simulate")
@click.argument('precinct_file', type=click.Path(exists=True))
@click.option('--num-booths', type=int, default=1,
              help="number of voting booths to use")
@click.option('--impatience-threshold', type=float,
              default=1000, help="the impatience threshold")
@click.option('--print-voters', is_flag=True)
@click.option('--find-threshold', is_flag=True)
@click.option('--find-num-booths', is_flag=True)
@click.option('--num-trials', type=int, default=100,
              help="number trials to run")
def cmd(precinct_file, num_booths, impatience_threshold,
        print_voters, find_threshold, find_num_booths, num_trials):
    """
    Run the program...
    """
    #pylint: disable=too-many-locals
    p, seed = util.load_precinct(precinct_file)

    precinct = Precinct(p["name"],
                        p["hours_open"],
                        p["num_voters"],
                        p["arrival_rate"],
                        p["voting_duration_rate"],
                        p["impatience_prob"])

    if find_threshold:
        pt = find_impatience_threshold(seed, precinct, num_booths, num_trials)
        s = ("Given {} booths, an impatience threshold of {}"
             " would be appropriate for Precinct {}")
        print(s.format(num_booths, pt, p["name"]))
    elif find_num_booths:
        vbn = find_voting_booths_needed(seed, precinct,
                                        impatience_threshold, num_trials)
        s = ("Given an impatience threshold of {}, provisioning {}"
             " booth(s) would be appropriate for Precinct {}")
        print(s.format(impatience_threshold, vbn, p["name"]))
    elif print_voters:
        vb = VotingBooths(num_booths)
        voters = precinct.simulate(seed, vb, impatience_threshold)
        util.print_voters(voters)
    else:
        vb = VotingBooths(num_booths)
        voters = precinct.simulate(seed, vb, impatience_threshold)
        print("Precinct", p["name"])
        print("- {} voters voted".format(len(voters)))
        if len(voters) > 0:
            # last person might be impatient.  look
            # backwards for the first actual voter.
            last_voter_departure_time = None
            for v in voters[::-1]:
                if v.departure_time:
                    last_voter_departure_time = v.departure_time
                    break
            s = "- Polls closed at {} and last voter departed at {:.2f}."
            print(s.format(p["hours_open"]*60, last_voter_departure_time))
            nv = len([v for v in voters if not v.has_voted])
            print("- {} voters left without voting".format(nv))
            if not voters[-1].departure_time:
                print("  including the last person to arrive at the polls")


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
