import data
#------Загрузка данных--------
all_data = data.load_data()
if "characters" not in all_data:
    all_data["characters"] = []
if "chapters" not in all_data:
    all_data["chapters"] = []
if "plot" not in all_data:
    all_data["plot"] = {"idea":"", "parts":[]}
characters = all_data["characters"]
chapters = all_data["chapters"]
plot = all_data["plot"]
parts = plot["parts"]
scene_fields = []
btn_x = []

#----состояние программы
is_dirty = False
selected_character_index = None
selected_chapter_index = None
selected_scenes_index = None
#Функция сохранения
def save_all():
    data.save_data(all_data)