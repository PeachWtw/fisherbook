from app.view_models.book import BookViewModel


class MyWishes:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()


    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            for wish_count in self.__wish_count_list:
                if gift.isbn == wish_count['isbn']:
                    temp_gifts.append(
                        {
                            "wishes_count":wish_count['count'],
                            "book": BookViewModel(gift.book),
                            "id":gift.id
                        }
                    )
        return temp_gifts
