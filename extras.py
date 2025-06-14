   @commands.command()
    async def update_sheet(self, ctx):
        """Command to create or update a Google Sheet"""
        # Check if an attachment is provided
        if not ctx.message.attachments:
            await ctx.send("Please attach a .csv file.")
            return

        # Check if the attachment is a .csv file
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.csv'):
            await ctx.send("Please attach a .csv file.")
            return

        # Read the attached .csv file
        try:
            csv_data = await attachment.read()
            csv_content = io.StringIO(csv_data.decode('utf-8'))
            csv_reader = csv.reader(csv_content)
            csv_rows = list(csv_reader)

            # Update the Google Sheet
            try:
                google_sheet = google_client.open_by_url(google_sheet_url)
                worksheet = google_sheet.sheet1  # Assume it's the first worksheet
                worksheet.clear()
                worksheet.update('A1', csv_rows)
                await ctx.send('Google Sheet updated successfully!')
            except Exception as e:
                await ctx.send(f'Failed to update Google Sheet: {e}')
                traceback.print_exc()
                print(f'Error updating Google Sheet: {e}')
        except Exception as e:
            await ctx.send(f"Failed to read the attached CSV file: {e}")



    @commands.command()
    async def update_sheet_api(self, ctx):
        """Command to fetch data from Clash of Clans API and update the Google Sheet"""
        # Fetch data from Clash of Clans API
        coc_api_url = 'https://api.clashking.xyz/war/%23gg2c8000/previous?timestamp_start=0&timestamp_end=2527625513&limit=3'
        clan_tag = '#gg2c8000'  # Replace with your clan tag
        encoded_clan_tag = urllib.parse.quote(clan_tag)
        coc_api_headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjI0N2MwNDgwLTcyNzgtNDhjMy05NDRhLTlkZGU3ODZlY2NlNCIsImlhdCI6MTcxMzM3NDY1Mywic3ViIjoiZGV2ZWxvcGVyL2I0OWYyNmQyLWEwMTAtYWQzMC1jN2VkLTYyYjA4MzRiOTFjMCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjQ1Ljc5LjIxOC43OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.uGquIrgSXkueQ5hxa9vQsPFDKmTtiEl-IaSMA_2JE4aa3x6I8b1n_TdoDFJi_j5Pbf9pOFW2cgTEyWCGgVWzLQ'}  # Replace with your Clash of Clans API key
        try:
            response = requests.get(coc_api_url)
            response_data = response.json()
            # print(response_data)
            if response.status_code != 200:
                await ctx.send(f"Failed to fetch data from Clash of Clans API: {response_data.get('message', 'Unknown error')}")
                return
        except Exception as e:
            print("error in 52")
            await ctx.send(f"Failed to fetch data from Clash of Clans API: {e}")
            return

        try:
            rows = []
            for clan in response_data:
                home_clan_tag = clan['clan']['tag']
                home_clan_name = clan['clan']['name']
                home_clan_level = clan['clan']['clanLevel']
                enemy_clan_tag = clan['opponent']['tag']
                enemy_clan_name = clan['opponent']['name']
                enemy_clan_level = clan['opponent']['clanLevel']
                
                for member in clan['clan']['members']:
                    member_tag = member['tag']
                    member_name = member['name']
                    th_level = member['townhallLevel']
                    
                    if 'attacks' in member:
                        for attack in member['attacks']:
                            attacker_tag = attack['attackerTag']
                            defender_tag = attack['defenderTag']
                            stars = attack['stars']
                            destruction_percentage = attack['destructionPercentage']
                            opponent_defender_tag = member['bestOpponentAttack']['defenderTag']
                            
                            row = [
                                member_tag,
                                member_name,
                                th_level,
                                attacker_tag,
                                defender_tag,
                                stars,
                                None,  # Placeholder for new_stars
                                destruction_percentage,
                                None,  # Placeholder for defender_th
                                1,  # Hardcoded value for attacker_is_home_clan
                                home_clan_tag,
                                home_clan_name,
                                home_clan_level,
                                enemy_clan_tag,
                                enemy_clan_name,
                                enemy_clan_level,
                                None,  # Placeholder for war_start_time
                                None,  # Placeholder for war_size
                                None   # Placeholder for type
                            ]
                            rows.append(row)
            
            # Iterate through rows to update defender_th
            for row in rows:
                defender_tag = row[4]
                for clan in response_data:
                    for member in clan['clan']['members']:
                        if member['tag'] == defender_tag:
                            row[8] = member['townhallLevel']
                            break  # Once found, no need to iterate further
                        
                    
        except Exception as e:
            print(e)
            await ctx.send(f"Failed to process data from Clash of Clans API: {e}")
            return

        # Update the Google Sheet
        try:
            worksheet = google_client.open_by_url(google_sheet_url).worksheet("Test_Sheet")
            # worksheet = google_sheet.sheet4  # Assume it's the first worksheet
            worksheet.clear()
            worksheet.update('A1', rows)
            await ctx.send('Google Sheet updated successfully!')
        except Exception as e:
            await ctx.send(f'Failed to update Google Sheet: {e}')
            traceback.print_exc()
            print(f'Error updating Google Sheet: {e}')
        

