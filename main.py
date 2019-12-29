import json
import datetime
import wx
from tag import Tag
from campaign_log_reader import CampaignLogReader
from tag_image_dialog import TagImageDialog

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        main_sizer.Add(self.create_left_sizer(), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.create_right_sizer(), 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(main_sizer)

    def create_left_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.file_picker = wx.FilePickerCtrl(self, 
            message="Bitte Log-Export auswählen", 
            wildcard="*.json",
            style=wx.FLP_OPEN|wx.FLP_FILE_MUST_EXIST)
            #style=wx.FLP_USE_TEXTCTRL|wx.FLP_SMALL)
        sizer.Add(self.file_picker, 0, wx.ALL , 5)
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.read_file)
        
        pFile = self.file_picker.GetPickerCtrl()
        pFile.SetLabel("Log-Datei auswählen")
        #pTextFile = self.file_picker.GetTextCtrl()
        #pTextFile.SetStyle(self, wx.TE_READONLY)

        # TODO add search (SearchCtrl)

        self.allTags_list_ctrl = wx.ListCtrl(
            self, size=(351, 450), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.create_columns(self.allTags_list_ctrl, 160, 120, 67)
        self.allTags_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.update_details, self.allTags_list_ctrl)
        sizer.Add(self.allTags_list_ctrl, 1, wx.ALL, 5) 

        return sizer

    def create_right_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.headline = wx.StaticText(self)
        font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        self.headline.SetFont(font) 
        self.headline.SetLabel("Kein Log geladen") 
        headerSizer.Add(self.headline, 1, wx.ALL|wx.EXPAND, 0)

        def on_click(self):
            with self.img_dialog as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    # do something here
                    print('Hello')
                else:
                    # handle dialog being cancelled or ended by some other button
                    print('Else')

                # The dialog is automatically destroyed on exit from the context manager
            #print("hallo")

        button = wx.Button(self, wx.ID_ANY, 'Bild', (10, 8))
        #self.Bind(wx.EVT_BUTTON, lambda event: on_click(event, self.selected_main_tag), button)
        button.Bind(wx.EVT_BUTTON, on_click)
        headerSizer.Add(button, 0, wx.ALL, 0)

        sizer.Add(headerSizer, 0, wx.ALL|wx.EXPAND, 6)

        self.linkedTags_list_ctrl = wx.ListCtrl(
            self, size=(351, 150), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.create_columns(self.linkedTags_list_ctrl, 160, 120, 67)
        self.linkedTags_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.update_linkedTags, self.linkedTags_list_ctrl)
        sizer.Add(self.linkedTags_list_ctrl, 1, wx.ALL, 5) 

        self.linkedTag_textbox = wx.TextCtrl(
            self, size=(351, 150), style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_WORDWRAP
        )
        self.linkedTag_textbox.SetEditable(False)
        sizer.Add(self.linkedTag_textbox, 2, wx.ALL, 5) 
        #self.entriesSizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.entriesSizer, 1, wx.ALL|wx.EXPAND, 5)

        return sizer

    def update_details(self, event):
        ind = event.GetIndex()
        item = self.allTags_list_ctrl.GetItem(ind, 0)
        id_of_row_tag = self.allTags_list_ctrl.GetItemData(ind)
        self.headline.SetLabelText(item.GetText())

        row_tag = self.table_objects[id_of_row_tag]
        self.selected_main_tag = row_tag.id
        self.img_dialog = TagImageDialog(self, "Passendes Bild")
        self.img_dialog.set_selected_tag(row_tag.id)
        linkedEntries = CampaignLogReader(self.data).createLinks(row_tag)
        #linkedEntries = CampaignLogReader(self.data).createLinks(self.tagsInTable[ind])
        #self.linkedPostsInTable = []
        self.linkedTags_list_ctrl.ClearAll()
        self.create_columns(self.linkedTags_list_ctrl, 160, 120, 50)

        index = 0
        for entry in linkedEntries:
            entryAsTag = Tag(entry)
            entryAsTag.count = len(linkedEntries[entry])

            #self.linkedPostsInTable.append(linkedEntries[entry])
            self.add_row(index, self.linkedTags_list_ctrl, entryAsTag, linkedEntries[entry])

            index += 1

        # *** try append to static TextCtrl ***
        #self.entriesSizer.Layout

    def update_linkedTags(self, event):
        ind = event.GetIndex()
        #item = self.linkedTags_list_ctrl.GetItem(ind, 0)
        id_of_row_posts = self.linkedTags_list_ctrl.GetItemData(ind)
        posts_of_row = self.table_objects[id_of_row_posts]

        self.linkedTag_textbox.Clear()
        #for post in self.linkedPostsInTable[ind]:
        for post in posts_of_row:

            # 2018-11-02T22:33:11.131Z -> 02.11.2018 22:33:11
            d = datetime.datetime.strptime(post[:-5], '%Y-%m-%dT%H:%M:%S')
            self.linkedTag_textbox.AppendText(datetime.date.strftime(d, "%d.%m.%y %H:%M:%S") + "\n")

            self.linkedTag_textbox.AppendText(posts_of_row[post] + "\n")
            self.linkedTag_textbox.AppendText("--------------------------------\n")

        self.linkedTag_textbox.SetInsertionPoint(0)


    def update_folder(self, folder_path):
        self.current_folder_path = folder_path
        print(f'Ausgewählter Pfad: "{folder_path}"')
        self.file_picker.SetPath(folder_path)

    def read_file(self, event):
        self.headline.SetLabelText("Keinen Eintrag ausgewählt")
        # store object ids for table rows
        self.table_objects = {} 

        with open(event.GetPath(), encoding='utf-8') as f:
            self.data = json.load(f)
            self.allTags = CampaignLogReader(self.data).readAllTags()

            # reset tag panel
            self.allTags_list_ctrl.ClearAll()
            self.create_columns(self.allTags_list_ctrl, 160, 120, 50)
            # reset detail panel
            self.linkedTags_list_ctrl.ClearAll()
            self.create_columns(self.linkedTags_list_ctrl, 160, 120, 50)
            self.linkedTag_textbox.Clear()

            index = 0
            #self.tagsInTable = []
            for tag in self.allTags:

                #self.tagsInTable.append(tag)
                self.add_row(index, self.allTags_list_ctrl, tag, tag)

                index += 1
    
    def create_columns(self, listCtrl, nameWth, typeWth, countWth):
        listCtrl.InsertColumn(0, 'Name', width=nameWth)
        listCtrl.InsertColumn(1, 'Typ', width=typeWth)
        listCtrl.InsertColumn(2, 'Anzahl', width=countWth)

    def add_row(self, index, list_ctrl, tag, data):
        list_ctrl.InsertItem(index, tag.name)
        list_ctrl.SetItem(index, 1, tag.type)
        list_ctrl.SetItem(index, 2, str(tag.count))

        id = int(wx.NewIdRef())
        self.table_objects[id] = data
        list_ctrl.SetItemData(index, id)


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None,
                         title='Campaign Log Analyzer', size=(800, 600))
        self.panel = MainPanel(self)
        #self.create_menu()
        icon_logo = wx.Icon("resources/cllogo.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon_logo)
        self.Layout()
        self.Show()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(
            wx.ID_ANY, 'Öffnen ...',
            'Campaign Log auswählen'
        )
        menu_bar.Append(file_menu, '&Datei')
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.on_open_folder,
            source=open_folder_menu_item,
        )
        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title,
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_folder(dlg.GetPath())
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
