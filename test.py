from flet import *
import flet as ft

def main(page: Page):
    page.scroll = "always"

    name = TextField(label="YOu name Here")
    youid = Text("")

    # CREATE DATATABLE HERE
    mytable = DataTable(
        columns=[
            DataColumn(Text("id")),
            DataColumn(Text("name")),
            DataColumn(Text("address")),
        ],
        # THIS IS YOU ROW OF YOU TABLE
        rows=[]

    )

    # GET ID THE ROW
    def editindex(e, r):
        print("you id is = ", e)
        print("you seledted name is = ", r)

        # SET NAME TEXTFIELD TO YOU SELECT THE ROW
        name.value = r
        youid.value = int(e)

        # HIDE THE ADD NEW BUTTON . AND TRUE OF EDIT AND DELETE BUTTON
        addButton.visible = False
        deleteButton.visible = True
        editbutton.visible = True
        page.update()

    # ADD DATA TO TABLE
    def addnewdata(e):
        mytable.rows.append(
            DataRow(
                cells=[
                    # THIS FOR ID THE YOU TABLE
                    DataCell(Text(len(mytable.rows))),
                    DataCell(Text(name.value)),
                    DataCell(Text("FAke address")),
                ],
                # IF YOU CLIK THIS ROW THEN RUN YOU FUNCTION
                # THIS SCRIPT IS IF CLICK THEN GET THE ID AND NAME OF ROW
                on_select_changed=lambda e: editindex(e.control.cells[0].content.value,
                                                      e.control.cells[1].content.value)
            )

        )
        # THEN BLANK AGAIN THE TEXTFIELD
        name.value = ""
        page.update()

    addButton = ElevatedButton("add new",
                               bgcolor="blue",
                               color="white",
                               on_click=addnewdata
                               )

    # EDIT THEN SAVE YOU DATA
    def editandsave(e):
        # THIS SCRIPT IS SELECT YOU DATA BEFORE AND
        # CHANGE TO NEW DATA FOR UPDATE IN TEXTFIELD

        mytable.rows[youid.value].cells[1].content = Text(name.value)
        page.update()

    # FINALLY DELETE YOU DATA FROM TABLE
    def removeindex(e):
        #print("you id is = ", youid.value)
        del mytable.rows[youid.value]

        # THEN SHOW SNACK BAR . THIS OPTIONAL
        page.snack_bar = SnackBar(
            Text(f"succes delete you id  = {youid.value}", color="white"),
            bgcolor="red",
        )
        page.snack_bar.open = True
        page.update()

    # DELETEBUTTON
    deleteButton = ElevatedButton("delete this",
                                  bgcolor="red",
                                  color="white",
                                  on_click=removeindex

                                  )

    # EDIT BUTTON
    editbutton = ElevatedButton("update data",
                                bgcolor="orange",
                                color="white",
                                on_click=editandsave

                                )

    # AND HIDE YOU EDIT BUTTON AND DELETE BUTTON
    # IF NOT EVENT TO EDIT AND DELETE
    # BY DEFAULT IS FALSE , EXCEPT ADDNEW BUTTON
    deleteButton.visible = False
    editbutton.visible = False

    page.add(
        Column([
            Text("my crud sample", size=30, weight="bold"),
            name,
            Row([addButton, editbutton, deleteButton]),
            mytable

        ])

    )


ft.app(target=main)