import wx
import wx.lib.mixins.listctrl  as  listmix

class OrderListControl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, size):
 
        wx.ListCtrl.__init__(self, parent, -1, size, 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.create_columns(160, 120, 67)

        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, self.GetColumnCount())

        self.table_objects = {}
        self.itemDataMap = {}

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self

    def create_columns(self, nameWth, typeWth, countWth):
        self.InsertColumn(0, 'Name', width=nameWth)
        self.InsertColumn(1, 'Typ', width=typeWth)
        self.InsertColumn(2, 'Anzahl', width=countWth)

    def add_row(self, index, tag, data):
        self.InsertItem(index, tag.name)
        self.SetItem(index, 1, tag.type)
        self.SetItem(index, 2, str(tag.count))

        id = int(wx.NewIdRef())
        self.itemDataMap[id] = (tag.name, tag.type, tag.count)
        self.table_objects[id] = data
        self.SetItemData(index, id)

    def empty_table(self):
        self.ClearAll()
        self.create_columns(160, 120, 50)
        self.itemDataMap = {}

    def get_row_object(self, index):
        id_of_row_object = self.GetItemData(index)
        return self.table_objects[id_of_row_object]

