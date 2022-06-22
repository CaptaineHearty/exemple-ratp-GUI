import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4

ApplicationWindow {
    id: root
    color: "#333333"
    visible: true
    width: 600
    height: 500
    title: "HelloApp"
    Material.accent: Material.Teal
    Material.theme: Material.Dark

    // Text {
    //     anchors.centerIn: parent
    //     text: "Bonjour"
    //     font.pixelSize: 24
    // }

    TextField {
        id: searchbar
        width: 300
        height: 60
        placeholderText: "Entrer une ligne de bus"
        x: root.width/2 - width/2
        y: 15
        onTextChanged: {
            busesModel.fetch_buses(text)
        } 
    }

    ComboBox {
        id: buses
        width: 300
        currentIndex: 0
        displayText: "Numéro de bus: " + currentText
        model: busesModel
        textRole: "name"
        x: root.width/2 - width/2
        y: root.height*0.2  
        onActivated: {
            let bus_code = busesModel.get_elem_at(index, 1)
            console.log("bus code = ", bus_code)
            stationsModel.fetch_stations(bus_code)
        }
    }

    ComboBox {
        id: stations
        width: 300
        currentIndex: 0
        displayText: "Nom de la station : " + currentText
        model: stationsModel
        textRole: "name"
        x: root.width/2 - width/2
        y: buses.y + buses.height + 20 
        onActivated: {
            let bus_code = busesModel.get_elem_at(buses.currentIndex, 1)
            console.log("bus code = ", bus_code)
            let station_code = stationsModel.get_elem_at(index, 1)
            console.log("sation code = ", station_code)
            etasModel.update(bus_code, station_code)
            refresh_button.enabled = true
        }
    }

    TableView{
        id: etas
        width: 300
        height: 300
        model: etasModel
        x:root.width/2 - width/2
        y:stations.y + stations.height + 20
        ScrollBar.vertical:ScrollBar{
            policy: ScrollBar.AsNeeded
        }
        delegate: Rectangle {
            implicitWidth: 150
            implicitHeight: 50
            color: "#333333"
            border.color: "#FFFFFF"
            border.width: 3
            Text {
                anchors.centerIn: parent
                text: display
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                color: "#FFFFFF"
            }
        }
 
    }

    BusyIndicator{
        id: busy_spin
        width: 50
        height: 50
        x: root.width-width-10
        y: 30
        running: myApi.spin_busy 
    }
// coordonées du bord haut : etas.y  bord bas : etas.y + etas.height  
    ToolButton{
        id: refresh_button
        width: 50
        height: 50
        x:  etas.width + etas.x + 10
        y: (etas.y + etas.y + 150)/2 - (height/2)
        icon.source: "qrc:/icons/refresh.svg"
        onClicked: {
            let bus_code = busesModel.get_elem_at(buses.currentIndex, 1)           
            if (bus_code == ""){
                console.log("Bus code invalide, refresh impossible")
                return 
            }
            let station_code = stationsModel.get_elem_at(stations.currentIndex, 1)
            if (station_code == ""){
                console.log("Station code invalide, refresh impossible")
                return
            }
            etasModel.update(bus_code, station_code)                
        }
        enabled: false 

    }
    


}
