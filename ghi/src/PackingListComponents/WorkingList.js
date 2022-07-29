import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

function WorkingList({
    items,
    setItems,
    destination_city,
    destination_country,
    departure_date,
    return_date,
}){
      
    function findItem(name) {
        for (let index = 0; index < items.length; index ++) {
            if (items[index].name === name) {
                return index
            }
        }
        return "item not found!"
    }

    function deleteItem(event) {
        const item_index = findItem(event.target.value)
        setItems([...items.filter((_, i) => i !== item_index)])
    };

    async function sendData(data, url) {
        const fetchConfig = {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            }
        };
        const response = await fetch(url, fetchConfig);
        if (response.ok) {
            const listData = await response.json();
            return listData

        } else {
            console.error(response.status);
        };
    }

    async function createList() {
        if (items.length > 0) {
            const packingListData = {
                "title": `Packing list for ${destination_city}, ${destination_country}`,
                "departure_date": departure_date,
                "return_date": return_date,
                "destination_city": destination_city,
                "destination_country": destination_country,
                "owner": 1,
            };
            const packingListUrl = "http://localhost:8005/api/packing_lists/"
            const packingList = await sendData(packingListData, packingListUrl)
            if (packingList) {
                const itemsData = {"items": items};
                const itemsUrl = `http://localhost:8005/api/packing_lists/${packingList.id}/items/`;
                const packingListItems = await sendData(itemsData, itemsUrl);
                console.log({"packingList": packingList, "items": packingListItems});
            }
        } else {
            console.log("you cant create an empty packing list")
        }
    }

    // const paragraph = document.getElementById("edit");
    // const edit_button = document.getElementById("edit-button");
    // const end_button = document.getElementById("end-editing");
    
    // edit_button?.addEventListener("click", function() {
    //   paragraph.contentEditable = true;
    //   paragraph.style.backgroundColor = "#dddbdb";
    // } );
    
    // end_button?.addEventListener("click", function() {
    //   paragraph.contentEditable = false;
    //   paragraph.style.backgroundColor = "white";
    // } )

    return (
        <div className="">
                <div id="container">
                    <h3 id="edit" > Packing List for {destination_country}</h3>
                    <button type="submit" id="edit-button">Edit</button>
                    <button type="submit" id="end-editing">Save</button>
                </div>
            <table className="table table-hover">
                <thead>
                    <tr>
                        <th className="text-center" style={{width: "90px"}}>QTY</th>
                        <th className="text-center">{items.length === 1 ? 'Item' : "Items"}</th>
                        <th className="text-center" style={{width: "10%"}}></th>
                    </tr>
                </thead>
                <tbody>
                    {items.map(item => {
                        return (<tr key={item.name}>
                            <td>
                                <input
                                    className="form-control form-control-sm"
                                    type="number"
                                    onChange={(event) => {
                                        const newItems = [...items];
                                        const index = findItem(item.name);
                                        newItems[index].quantity = event.target.value;
                                        setItems(newItems);
                                    }}
                                    defaultValue={item.quantity}
                                    min={1}
                                    max={1000}
                                />
                            </td>
                            <td>{item.suggested ? item.name + " (suggested)" : item.name}</td>
                            <td>
                                <button
                                    className="btn btn-sm btn-outline-danger"
                                    onClick={deleteItem}
                                    value={item.name}
                                >
                                    <FontAwesomeIcon icon={faTrash}/>
                                </button>
                            </td>
                        </tr>)
                    })}
                </tbody>
            </table>
            <div>
                <button className="btn btn-success" onClick={createList}>Create!</button>
            </div>
        </div>
    );
};

export default WorkingList;
