import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:

    def button_start_clicked_cb(self, button):
        print('Start')

    def button_open_project_clicked_cb(self, button):
        print('Project')

    def window_main_delete_event_cb(self, *args):
        Gtk.main_quit(*args)




if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file("main.glade")
    builder.connect_signals(Handler())

    window = builder.get_object("window_main")
    window.show_all()

    Gtk.main()
