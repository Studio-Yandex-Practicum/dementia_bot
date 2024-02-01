import datetime

from services.answers import RESULTS

from botapp.services.countries_list.ru_set import COUNTRIES_NAMES
from botapp.services.image_neural_handler.onnx_inference import get_image_score


class TestService:
    CORRECT_ANSWER_15 = ("носорог", "арфа")
    CORRECT_ANSWER_16 = ("цветы", "цветок", "растения", "растение", "природа", "флора")
    CORRECT_ANSWER_17 = ("6", "шесть")
    CORRECT_ANSWER_18 = ("1 рубль 95 копеек", "1,95", "1.95", "01,95", "01.95", "01 рубль 95 копеек")
    CORRECT_ANSWER_23 = "1А2Б3В4Г5Д6Е"
    CORRECT_ANSWER_24 = ("3,4,5,6,7,8,9", "1,2,3,4,5,6,7")
    CORRECT_ANSWER_25 = ("я закончила", "я закончил")
    EMAIL_FROM_ANSWER = 4

    def question_14(answer: str, *args) -> int:
        """Назовите сегодняшнюю дату, месяц, год."""
        result = 0
        date_obj = datetime.datetime.strptime(answer, "%d-%m-%Y").date()
        today = datetime.date.today()
        three_days = datetime.timedelta(3)
        if date_obj == today:
            result += 2
        elif today - three_days <= date_obj <= today + three_days:
            result += 1
        if date_obj.month == today.month:
            result += 1
        if date_obj.year == today.year:
            result += 1
        return result

    def question_15(answer: str, *args) -> int:
        """Назовите объекты, изображённые на рисунках."""
        result = 0
        treated_answer = [x.lower().strip() for x in answer.split(",")]
        if treated_answer[0] == TestService.CORRECT_ANSWER_15[0]:
            result += 1
        if treated_answer[1] == TestService.CORRECT_ANSWER_15[1]:
            result += 1
        return result

    def question_16(answer: str, *args) -> int:
        """Что общего между розой и тюльпаном?"""
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_16:
            return 2
        return 0

    def question_17(answer: str, *args) -> int:
        """Сколько полтинников в 3 рублях?"""
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_17:
            return 1
        return 0

    def question_18(answer: str, *args) -> int:
        """
        Вы оплачиваете в кассу 3 рубля 05 копеек?
        Сколько сдачи вы получите, если дадите кассиру 5 рублей?
        """
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_18:
            return 1
        return 0

    def question_19(answer: str, *args) -> int:
        return 0

    def question_20(answer: str, *args) -> int:
        """Скопируйте рисунок."""
        return get_image_score("figure", args[0])

    def question_21(answer: str, *args) -> int:
        """Нарисуйте циферблат и разместите на нем цифры."""
        return get_image_score("clock", args[0])

    def question_22(answer: str, *args) -> int:
        """Напишите названия 12 разных стран."""
        result = set()
        answer = answer.replace(" ", "")
        answer = answer.replace("-", "")
        countries = {item.lower() for item in answer.split(",")}
        for country in countries:
            tmp = COUNTRIES_NAMES.get(country, "False")
            if tmp != "False":
                if tmp == "":
                    result.add(country)
                else:
                    result.add(tmp)
        result = len(result)
        if result == 12:
            return 2
        if result in (10, 11):
            return 1
        return 0

    def question_23(answer: str, *args) -> int:
        """Прочертите между кругами линию."""
        mistakes = 0
        zipped_answers = zip(answer, TestService.CORRECT_ANSWER_23)
        for user_answ, expected_answ in zipped_answers:
            if user_answ != expected_answ:
                mistakes += 1
        if not mistakes:  # без ошибок
            return 2
        if mistakes in (1, 2):  # 1-2 ошибки
            return 1
        return 0

    def question_24(answer: str, *args) -> int:
        """На рисунке четыре треугольника. Удалите 2 линии[...]"""
        if answer in TestService.CORRECT_ANSWER_24:
            return 2
        return 0

    def question_25(answer: str, *args) -> int:
        """Вы всё сделали?"""
        treated_answer = answer.lower().strip()
        if treated_answer in TestService.CORRECT_ANSWER_25:
            return 2
        return 0


class TestServiceRelative:
    EMAIL_FROM_ANSWER = 5

    def question_6(answer: str, *args) -> int:
        """У близкого Вам человека есть проблемы с памятью?"""
        result = RESULTS[6].get(answer, 0)
        return result

    def question_7(answer: str, *args) -> int:
        """Если это так, стала память хуже, чем несколько лет назад?"""
        result = RESULTS[7].get(answer, 0)
        return result

    def question_8(answer: str, *args) -> int:
        """
        Ваш близкий повторяет один и тот же вопрос или высказывает одну
        и ту же мысль несколько раз в течение дня?
        """
        result = RESULTS[8].get(answer, 0)
        return result

    def question_9(answer: str, *args) -> int:
        """Забывает ли он о назначенных встречах или событиях?"""
        result = RESULTS[9].get(answer, 0)
        return result

    def question_10(answer: str, *args) -> int:
        """Кладет ли он вещи в непривычные места чаще 1 раза в месяц?"""
        result = RESULTS[10].get(answer, 0)
        return result

    def question_11(answer: str, *args) -> int:
        """
        Подозревает ли близких в том, что они прячут или крадут его вещи,
        когда не может найти их?
        """
        result = RESULTS[11].get(answer, 0)
        return result

    def question_12(answer: str, *args) -> int:
        """
        Часто ли он испытывает трудности
        при попытке вспомнить текущий день недели, месяц, год?
        """
        result = RESULTS[12].get(answer, 0)
        return result

    def question_13(answer: str, *args) -> int:
        """Он испытывает проблему с ориентацией в незнакомом месте?"""
        result = RESULTS[13].get(answer, 0)
        return result

    def question_14(answer: str, *args) -> int:
        """Усиливается ли рассеянность за пределами дома, в поездках?"""
        result = RESULTS[14].get(answer, 0)
        return result

    def question_15(answer: str, *args) -> int:
        """Возникают ли проблемы при подсчете сдачи в магазине?"""
        result = RESULTS[15].get(answer, 0)
        return result

    def question_16(answer: str, *args) -> int:
        """Есть ли трудности с оплатой счетов, финансовых операций?"""
        result = RESULTS[16].get(answer, 0)
        return result

    def question_17(answer: str, *args) -> int:
        """
        Забывает ли он принимать лекарства?
        Были случаи, когда он не мог вспомнить, принимал ли он уже лекарство?
        """
        result = RESULTS[17].get(answer, 0)
        return result

    def question_18(answer: str, *args) -> int:
        """Есть ли проблемы с управлением автомобилем?"""
        result = RESULTS[18].get(answer, 0)
        return result

    def question_19(answer: str, *args) -> int:
        """
        Возникают ли трудности при пользовании бытовыми приборами,
        телефоном, телевизионным пультом?
        """
        result = RESULTS[19].get(answer, 0)
        return result

    def question_20(answer: str, *args) -> int:
        """Испытывает ли он затруднения, выполняя работу по дому?"""
        result = RESULTS[20].get(answer, 0)
        return result

    def question_21(answer: str, *args) -> int:
        """Потерял ли он интерес к привычным увлечениям?"""
        result = RESULTS[21].get(answer, 0)
        return result

    def question_22(answer: str, *args) -> int:
        """Может ли Ваш близкий потеряться на знакомой территории
        (например, рядом с собственным домом)?
        """
        result = RESULTS[22].get(answer, 0)
        return result

    def question_23(answer: str, *args) -> int:
        """Утрачивает ли чувство правильного направления движения?"""
        result = RESULTS[23].get(answer, 0)
        return result

    def question_24(answer: str, *args) -> int:
        """
        Случается, ли, что Ваш близкий не только забывает имена,
        но и не может вспомнить нужное слово?
        """
        result = RESULTS[24].get(answer, 0)
        return result

    def question_25(answer: str, *args) -> int:
        """Путает ли Ваш близкий имена родственников или друзей?"""
        result = RESULTS[25].get(answer, 0)
        return result

    def question_26(answer: str, *args) -> int:
        """Есть ли у него проблемы с узнаванием знакомых людей?"""
        result = RESULTS[26].get(answer, 0)
        return result
