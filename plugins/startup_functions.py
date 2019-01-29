import plugins


async def startup_lunch_scheduler(client):
    await plugins.lunch.run_lunch_scheduler(client)


# async def startup_cake_scheduler(client):
#     import plugins.cake.cake
#     await plugins.cake.cake.run_cake_scheduler(client)
