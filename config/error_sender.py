import discord

async def send(target, embed):
    # Envía un embed a un Context o a un Interaction
    if isinstance(target, discord.Interaction):
        try:
            if not target.response.is_done():
                await target.response.send_message(embed=embed)
            else:
                await target.followup.send(embed=embed)
        except Exception:
            # Fallback: intenta enviar al usuario por DM
            try:
                await target.user.send(embed=embed)
            except Exception:
                pass
    else:
        await target.send(embed = embed)
