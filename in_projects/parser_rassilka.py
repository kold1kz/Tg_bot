new_games = sg.new_games()
        if(new_games):
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game.info(ng)
            subscriptions = db.get_subscriptions()
            with open(sg.download_image(nfo['image']), 'rb') as photo:
                for s in subscriptions:
                    await bot.send_photo(
                        s[1],
                        photo,
                        caption= nfo['title'] +"\n"+"Оценка"+nfo['score']+"\n"+nfo['excerpt']+"\n\n"+nfo['link'],
                        disable_notification = True
                    )
            sg.update_lastkey(nfo['id'])