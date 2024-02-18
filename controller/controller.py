from model import engine, UserDb, Media, Category
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class User:
    '''This class will take all the parameters needed for shaping the User.
    Such as password, email and name.'''
    def _get_name(self) -> str:
        name = self.validate_name('Enter your name: ').title()
        return name

    def __set_name(self) -> None:
        self.name = self._get_name()

    def _get_email(self) -> str:
        while True:
            email = str(input('Enter your email: ')).lower().strip()
            if email == '' or len(email) < 5: 
                print('\033[31mPlease, type a valid email address.\033[m')
                continue
            elif not '@' in email:
                email += '@gmail.com'
            return email
    
    def __set_email(self) -> None:
        while True:
            email = self._get_email()
            try:
                exists = session.query(UserDb).filter(
                    UserDb.email == email).first() is not None
                session.close()
                if exists: raise ValueError
                self.email = email
                break
            except:
                print(f'\033[31mEMAIL ALREADY EXISTS, PLEASE CHOOSE A NEW ONE\033[m')
                continue

    def _get_password(self, text) -> str:
        import re
        from hashlib import sha256
        import getpass
        while True:
            password = getpass.getpass(prompt=f'{text}', stream=None)
            if len(password) < 8:
                print('\033[31mYour password MUST have at least 8 characteres.\033[m')
                continue
            elif not re.search("[a-z]", password):
                print('\033[31mYour password MUST have at least one lower case letter.\033[m')
                continue
            elif not re.search("[A-Z]", password):
                print('\033[31mYour password MUST have at least one upper case letter.\033[m')
                continue
            elif not re.search("[0-9]", password):
                print('\033[31mYour password MUST have at least one number.\033[m')
                continue
            else:
                encrypted_password = sha256(password.encode())
                return encrypted_password.hexdigest()

    def __set_password(self) -> None:
        self.password = self._get_password('Type your password: ')
        
    def _get_plan(self) -> str:
        plan_list = [{'id': '1', 'name': 'Basic', 'price': '€ 9'},
            {'id': '2', 'name': 'Regular', 'price': '€ 15'},
            {'id': '3', 'name': 'Premium', 'price': '€ 25'}]
        while True:
            print(f'\033[1;42m{"ID":<3}{"PLAN":<10}{"PRICE":<5}\033[m')
            [print(f'{plan["id"]:<3}{plan["name"]:<10}{plan["price"]:<5}')
             for plan in plan_list]
            try:
                plan = int(input('Choose your plan: '))
                assert 1 <= plan <= 3
            except:
                print('\033[31mPLEASE, CHOOSE A VALID OPTION\033[m')
            else:
                if plan == 1: return 'Basic'
                elif plan == 2: return 'Regular'
                elif plan == 3: return 'Premium'

    def __set_plan(self) -> None:
        self.plan = self._get_plan()

    def _check_email(self) -> bool:
        given_email = self._get_email()
        exists = session.query(UserDb).filter(
            UserDb.email == given_email).first()
        session.close() 
        if exists != None: return exists.id
        return 0

    def _encrypt_password(self) -> str:
        from hashlib import sha256
        import getpass
        password = getpass.getpass(prompt='Type your password: ', stream=None)
        encrypt_password = sha256(password.encode()).hexdigest()
        return encrypt_password

    def create_user(self) -> None:
        self.__set_name()
        self.__set_email()
        self.__set_password()
        self.__set_plan()

    def validate_name(self, message) -> str:
        while True:
            try:
                data = str(input(message)).strip()
                if data == '': raise ValueError
                for letter in data:
                    if not letter.isalpha() and not letter.isspace(): raise ValueError
            except:
                print(f'\033[31mINVALID VALUE\033[m')
                continue
            else:
                return data
            

class SystemManagement:

    def create_user(self) -> None:
        user = User()
        user.create_user()
        self.__register_user(user)

    def __register_user(self, user) -> None:
        user = UserDb(name=user.name,
                    email=user.email,
                    password=user.password,
                    plan=user.plan)
        self.__insert_data(user)
    
    def __insert_data(self, user) -> None:
        try:
            session.add(user)
        except:
            print(f'033[31mERROR, {user.name.upper()} NOT ADDED\033[m')
            session.rollback()
        else:
            print(f'\033[32m{user.name.upper()} SUCCESSFULLY ADDED\033[m')
            session.commit()
        finally:
            session.close()

    def sign_in(self) -> str:
        while True:
            try:
                id_user = User()._check_email()
                if id_user == 0: raise ValueError
            except:
                print(f'\033[31mEMAIL NOT FOUND\033[m')
                continue
            else:
                break
        password = User()._encrypt_password()
        try:
            user = session.query(UserDb).filter(UserDb.id == id_user).first()
            if user.password == password: return user
            raise ValueError
        except:
            print('\033[31mWRONG PASSWORD\033[m')
            return 0

    def watch_movie(self, user) -> None:
        from time import sleep
        category = MediaManagement()._choose_category()
        movies = session.query(Media).filter(Media.category == category).all()
        chosen_movie = self.__choose_id(movies)
        if user.plan == 'Basic' and chosen_movie["plan"] == 'Regular':
            print(f'\033[31mYou cannot access this movie', end=' ')
            print(f'with a {user.plan} plan.', end=' ')
            print(f'Please upgrade your plan.\033[m')
        elif user.plan == 'Basic' and chosen_movie["plan"] == 'Premium':
            print(f'\033[31mYou cannot access this movie', end=' ')
            print(f'with a {user.plan} plan.', end=' ')
            print(f'Please upgrade your plan.\033[m')
        elif user.plan == 'Regular' and chosen_movie["plan"] == 'Premium':
            print(f'\033[31mYou cannot access this movie', end=' ')
            print(f'with a {user.plan} plan.', end=' ')
            print(f'Please upgrade your plan.\033[m')
        else:
            print(f'Your chosen movie was \033[1;32m{chosen_movie["movie"].upper()}.\033[m', end=' ')
            print(f'The player is loading...')
            sleep(2)

    def __choose_id(self, movies: object) -> str:
        while True:
            try:
                print(f'\033[1;42m{"ID":<3}{"PLAN":<10}{"MOVIE NAME":<50}\033[m')
                movie_info = []
                biggest_id = 0
                for c, movie in enumerate(movies):
                    print(f'{c+1:<3}{movie.plan:<10}{movie.name:<50}')
                    movie_info.append({'number': c+1,
                                        'movie': movie.name,
                                        'id': movie.id,
                                        'plan': movie.plan})
                    if biggest_id < (c+1): biggest_id = (c+1)
                escolha = int(input('Enter the ID of the chosen movie: '))-1
                assert escolha < biggest_id
            except:
                print('\033[31mINVALID OPTION\033[m')
            else:
                return movie_info[escolha]

    def upgrade_plan(self, user: User) -> None:
        new_plan = User()._get_plan()
        session.query(UserDb).filter(UserDb.id == user.id).update({"plan": new_plan})
        print(f'\033[32mCONGRATULATIONS.', end=' ')
        print(f'You changed your plan to {new_plan}.\033[m')
        session.commit()


class MediaManagement:

    def add_category(self) -> None:
        category = User().validate_name('Enter the name of the category: ').title()
        self.__insert_category(category)

    def __insert_category(self, data) -> None:
        try:
            category = Category(name=data)
            session.add(category)
        except:
            print(f'\033[31m{category.name.upper()} NOT ADDED. TRY AGAIN.\033[m')
            session.rollback()
        else:
            print(f'\033[32m{category.name.upper()} SUCCESSFULLY ADDED\033[m')
            session.commit()
        finally:
            session.close()

    def add_movie(self) -> None:
        movie = User().validate_name('Enter the name of the movie: ').title()
        movie_category = self._choose_category()
        movie_plan = User()._get_plan()
        media = Media(name=movie,
                      plan=movie_plan,
                      category=movie_category)
        self.__insert_media(media)
    
    def __insert_media(self, media) -> None:
        try:
            session.add(media)
        except:
            print(f'\033[31m{media.name.upper()} NOT ADDED. TRY AGAIN.\033[m')
            session.rollback()
        else:
            print(f'\033[32m{media.name.upper()} SUCCESSFULLY ADDED\033[m')
            session.commit()
        finally:
            session.close()

    def _choose_category(self) -> int:
        data = session.query(Category).all()
        while True:
            print(f'\033[1;42m{"ID":<3}{"CATEGORY":<50}\033[m')
            [print(f'{line.id:<3}{line.name:<}') for line in data]
            try:
                category_number = int(input('Enter the number of the category: '))
                exists = session.query(Category).filter(
                    Category.id == category_number).first()
                if not exists: raise ValueError
            except:
                print('\033[31mINVALID OPTION\033[m')
            else:
                session.close()
                return exists.name

class Menu:

    def main_menu(self) -> None:
        menu = f"""\033[1;46m{"MAIN MENU":^100}\033[m
[1] CREATE USER
[2] SIGN IN
[3] EXIT"""
        text = f'Enter your option: '
        while True:
            choice = self.__get_option(menu, text, 3)
            match choice:
                case 1: SystemManagement().create_user()
                case 2: 
                    user = SystemManagement().sign_in()
                    if user != 0: self.menu_user(user)
                    continue
                case 3:
                    print('See you soon...')
                    break
        
    def menu_user(self, user) -> None:
        menu = f"""\033[1;46m{f"{user.name.upper()} MENU":^100}\033[m
[1] WATCH MOVIE
[2] UPGRADE PLAN
[3] EXIT"""
        text = f'Enter your option: '
        while True:
            choice = self.__get_option(menu, text, 3)
            match choice:
                case 1: SystemManagement().watch_movie(user)
                case 2: 
                    SystemManagement().upgrade_plan(user)
                    break
                case 3:
                    print('See you soon...')
                    break

    def __get_option(self, menu: str, text: str, range: int) -> int:
        while True:
            try:
                print(menu)
                choice = int(input(text))
                assert 1 <= choice <= range
            except:
                print('\033[31mINVALID OPTION\033[m')
            else:
                return choice
