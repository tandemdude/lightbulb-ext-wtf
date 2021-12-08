### Lightbulb WTF

This is a joke project (but working somehow).

I just wanted to mess around to see how much I could mess with lightbulb command declaration syntax.

## Usage

Commands are declared like generics using square brackets (`[]`) as the construction method.

A basic command:

```python
import lightbulb
from wtf import *

bot = lightbulb.BotApp(...)

async def foo_callback(ctx):
    await ctx.respond("Bar")


cmd = Command[
    Implements[lightbulb.PrefixCommand],
    Name["foo"],
    Description["test command"],
    Executes[foo_callback]
]

bot.command(cmd)
bot.run()
```
