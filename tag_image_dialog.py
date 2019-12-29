import wx

class TagImageDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(TagImageDialog, self).__init__(parent, title = title, size = (250,150))
        panel = wx.Panel(self)
        #self.btn = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,20), pos = (75,50))
        #super().__init__(self)
        print("I'm alive! :-D")

    def set_selected_tag(self, selectedTag):
        self.selectedTag = selectedTag

    def __enter__(self):
        print("You entered me! <3")
        # FIXME '*' und ' ' durch '_' ersetzen um legalen Dateinamen zu erhalten
        # TODO Bezug zu geladener Datei, also Log, herstellen (Unterordner?)

        #img_path = "images/" + self.selectedTag + ".jpg"
        img_path = "images/jeanluchs.jpg"
        wx.Image(img_path, type=wx.BITMAP_TYPE_ANY, index=-1)
        try:
            img = wx.Image(img_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            # bitmap upper left corner is in the position tuple (x, y) = (5, 5)
            bitmap = wx.StaticBitmap(self, -1, img, (10 + img.GetWidth(), 5), (img.GetWidth(), img.GetHeight()))

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(bitmap, 1, wx.ALL|wx.EXPAND, 6)
        except IOError:
            print("Image file %s not found" % img_path)

    def __exit__(self, *args):
        print("You left me! :´-(")

