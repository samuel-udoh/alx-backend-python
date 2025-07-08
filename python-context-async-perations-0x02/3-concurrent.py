import asyncio
import aiosqlite

async def async_fetch_users():
    query= "SELECT * FROM users"
    async with aiosqlite.connect('users.db') as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(query)
        users = await cursor.fetchall()
        await cursor.close()
        return users

async def async_fetch_older_users():
    query="SELECT * FROM users WHERE age > 40"
    connection = await aiosqlite.connect("users.db")
    connection.row_factory = aiosqlite.Row
    cursor = await connection.execute(query)
    older_user = await cursor.fetchall()
    await cursor.close()
    await connection.close()
    return older_user

async def fetch_concurrently():

    all_user, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    print("All Users")
    for user in all_user:
        print(f"ID: {user['user_id']}, Name: {user['first_name']}, Age: {user['age']}")

    print("\nOlder users:")
    for user in older_users:
        print(f"ID: {user['user_id']}, Name: {user['first_name']}, Age: {user['age']}")


if __name__=="__main__":
    asyncio.run(fetch_concurrently())