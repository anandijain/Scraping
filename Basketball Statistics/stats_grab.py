import os.path
import bs4

from open_functions import open_page
from open_functions import open_file

root_url = "https://www.basketball-reference.com"

"""
TODO:
attendence append/grab
"""


def lead_changes_count_grab(game_url, file):
    lead_change_link = url_pbp_alter(root_url + game_url)
    page = open_page(lead_change_link)     # get the website
    all_lead_changes = page.find_all("td", {"class": "bbr-play-leadchange center"})
    change_count = str(len(all_lead_changes))
    file.write(change_count + ",")
    print(change_count + "\n")


def url_pbp_alter(url_to_change):
    page = open_page(url_to_change)
    url_to_pbp = page.find("div", {"class": "filter"}).find_all("div")
    pbp = url_to_pbp[1].find('a', href=True)
    complete_pbp = "https://www.basketball-reference.com" + pbp['href']
    return complete_pbp


def header_grab(table, file):
    thead = table.thead
    header = thead.find_all("tr")[1].find_all("th")
    for column in header:
        header_text = column.text
        data_stat_text = column['data-stat']
        # print(column)
        if column['data-stat'] == 'game_result':
            file.write("w_l" + ",")
            file.write("Home Score" + ",")
            file.write("Away Score" + ",")
            continue
        if column['data-stat'] == 'game_location':
            continue
        if column['data-stat'] == 'date_game':
            file.write(header_text + ",")
            file.write("lead_changes" + ",")
            continue
        # print(header_text + ",")
        file.write(data_stat_text + ",")
    print("\n")
    file.write("\n")


def win_loss_separate(td, file):
    # print(td.text)
    win_loss = td.text.split(" ")[0]
    print(win_loss + " ,")

    scores = td.text.split(" ")[1]
    # print(scores + ",")

    home_score = scores.split("-")[0]
    print(home_score + " ,")

    away_score = scores.split("-")[1]
    print(away_score + " ,")

    file.write(win_loss + " ,")
    file.write(home_score + " ,")
    file.write(away_score + " ,")


def table_grab(data, file):
    i = 0
    for row in data:
        row_class = row.get('class')
        if row_class is not None:
            continue
        else:
            game_num = str(row.find("th").text)
            if game_num == "Rk":
                continue
            print(game_num + " ,")
            file.write(game_num + " ,")
            tds = row.find_all("td")

            for td in tds:
                text = str(td.text)
                if td['data-stat'] == "date_game":
                    file.write(text + ",")
                    game_url = td.a['href']
                    lead_changes_count_grab(game_url, file)
                    continue
                if td['data-stat'] == "game_result":
                    win_loss_separate(td, file)
                    continue
                if td['data-stat'] == "game_location":
                    continue
                file.write(text + ",")
            file.write("\n")
            i += 1


def next_page_grab(container, file):
    next_page = container.p.find("a", href=True, text="Next page")
    if next_page is not None:
        next_page_link = root_url + next_page['href']
        stats_grab(next_page_link, file)


def stats_grab(url, file):
    page = open_page(url)
    container = page.find("div", {"class": "p402_premium"})
    table = container.find("table", {"id": "stats"})
    data = table.find_all("tr")
    table_grab(data, file)
    next_page_grab(container, file)


def stats_grab_caller(url, file_name):
    page = open_page(url)
    file = open_file(file_name)
    container = page.find("div", {"class": "p402_premium"})
    table = container.find("table", {"id": "stats"})
    data = table.find_all("tr")
    header_grab(table, file)
    stats_grab(url, file)
    file.close()


# stats_grab("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2018&year_max=2018&is_range=N&game_num_type=team&game_location=H&order_by=date_game&order_by_asc=Y", "2018statsgrab2")
stats_grab_caller("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2015&year_max=2019&is_range=N&game_num_type=team&game_location=H&order_by=date_game", "all_stats_and_count5")


# stats_grab_caller("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2019&year_max=2019&is_range=N&game_num_type=team&game_location=H&order_by=date_game", "2018_all_stats_grab")
# stats_grab_caller("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2018&year_max=2018&is_range=N&game_num_type=team&game_location=H&order_by=date_game", "2017_all_stats_grab")
# stats_grab_caller("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2017&year_max=2017&is_range=N&game_num_type=team&game_location=H&order_by=date_game", "2016_all_stats_grab")
# stats_grab_caller("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2016&year_max=2016&is_range=N&game_num_type=team&game_location=H&order_by=date_game", "2015_all_stats_grab")
# stats_grab_caller("https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2015&year_max=2015&is_range=N&game_num_type=team&game_location=H&order_by=date_game", "2014_testing_data")
