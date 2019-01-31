from app.view_models.book import BookViewModel


class GiftSingle:
    def __init__(self,wishes_count,book,id):
        self.wishes_count = wishes_count
        self.book = book
        self.id = id

class GiftsCollections:
    def __init__(self,gifts_of_mine,wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.__parse()

    def __parse(self):
        for gift in self.__gifts_of_mine:
            for wish_count in self.__wish_count_list:
                if gift.isbn == wish_count['isbn']:
                    self.gifts.append(
                        GiftSingle(wish_count['count'],BookViewModel(gift.book),gift.id))


