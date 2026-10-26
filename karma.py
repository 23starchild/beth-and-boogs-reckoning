#!/usr/bin/env python3
"""
karma.py — a model of karma (Python 3).

What this is: a small simulation of cause and effect. An action puts a
weight on the ledger; the weight ripens into a consequence for the one
who acted; amends repair the balance.

The demo runs the facts as the Commander ruled them (2026-10-25):
Bethany, Boog, and Marc'O as agents; the ledger states what happened
plainly. Karma here means fair consequence and repair — not harm, not
revenge, not punishment dealt out by anyone else.

Run: python3 karma.py
"""

from dataclasses import dataclass, field

# Modeling choice (ZTeam N1): the Commander said Bethany hurt Marc'O
# "several times" — no number given. 3 is the author's choice, stated
# here so it is never mistaken for his number.
HURT_TIMES = 3


@dataclass
class Agent:
    name: str
    balance: int = 0          # + = goodwill earned, - = repair owed
    history: list = field(default_factory=list)

    def act(self, action: str, weight: int, target: "Agent | None" = None):
        """Do something. weight: +1 kind, -1 unkind. The ledger remembers."""
        self.balance += weight
        who = f" -> {target.name}" if target else ""
        self.history.append(f"{self.name} {action}{who} ({weight:+d})")
        print(f"  {self.name} {action}{who}  [{weight:+d}]  balance now {self.balance:+d}")

    def amend(self):
        """Take responsibility and repair. Only repair moves a negative
        balance back toward zero — the consequence is answered, not
        erased by time alone."""
        if self.balance < 0:
            self.balance += 1
            self.history.append(f"{self.name} made amends (+1)")
            print(f"  {self.name} made amends  [+1]  balance now {self.balance:+d}")
        else:
            print(f"  {self.name} has nothing to repair (balance {self.balance:+d})")

    def consequence(self):
        """What the balance means right now."""
        if self.balance > 0:
            return f"{self.name}: goodwill earned ({self.balance:+d}) — trust grows."
        if self.balance < 0:
            return f"{self.name}: repair owed ({self.balance:+d}) — amends are due."
        return f"{self.name}: balanced (0) — nothing owed, nothing earned."


def demo():
    # The facts, as the Commander ruled them 2026-10-25 ~23:20 EDT:
    # Bethany hurt Marc'O several times, never made amends or said sorry,
    # chose Boog over him, and ran his name through the mud.
    # Boog was supposed to be Marc'O's friend, then got with Bethany, the
    # girl Marc'O loved, and started rumors that Marc'O robbed him.
    # The ledger states them plainly. It inflicts nothing — the
    # consequence is repair owed, not harm.
    bethany = Agent("Bethany")
    boog = Agent("Boog")
    marco = Agent("Marc'O")

    print("KARMA — Actions, consequences, amends.\n")

    print("Round 1 — actions:")
    marco.act("called 911 for", +1, bethany)      # Oct 15, DKA
    marco.act("offered shelter to", +1, bethany)  # Oct 19, no strings
    for _ in range(HURT_TIMES):
        bethany.act("hurt", -1, marco)
    bethany.act("chose Boog over Marc'O", -1)
    bethany.act("ran Marc'O's name through the mud", -1)
    # NOTE (ZTeam N6): Boog's broader characterization (lies, steals,
    # wrecks homes/families, borrows money never pays it back, never
    # showers) is NOT encoded here — encoding e.g. "steals" as a -1
    # against Marc'O would invent a victim. Only the acts against
    # Marc'O are on the ledger. Deliberate; ZTeam agreed.
    boog.act("betrayed the friendship of", -1, marco)
    boog.act("got with Bethany, the girl Marc'O loved", -1)
    boog.act("spread rumors that Marc'O robbed him", -1)

    print("\nConsequences ripen:")
    print(" ", marco.consequence())
    print(" ", bethany.consequence())
    print(" ", boog.consequence())

    print("\nRound 2 — amends:")
    print("  Bethany made no amends, said no sorry.")
    print("  No amends from Boog on record.")
    marco.amend()

    print("\nFinal standing:")
    print(" ", marco.consequence())
    print(" ", bethany.consequence())
    print(" ", boog.consequence())

    print("\nLedger (full history):")
    for agent in (marco, bethany, boog):
        print(f"  {agent.name}:")
        for entry in agent.history:
            print(f"    {entry}")


def mechanism_check():
    """Exercises the amend() path the facts demo never touches: a
    negative balance cleared one amend at a time. Scratch agent only —
    not the facts (ZTeam N3)."""
    print("\nMechanism check (scratch agent, not the facts):")
    test = Agent("Test")
    test.act("did harm", -1)
    test.act("did harm", -1)
    print(" ", test.consequence())
    test.amend()
    test.amend()
    print(" ", test.consequence())
    assert test.balance == 0, "amend() did not clear the balance"
    print("  amend() path verified: -2 -> 0 in two amends.")


if __name__ == "__main__":
    demo()
    mechanism_check()
