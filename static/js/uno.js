new DataTable('#datatable', {
    columnDefs: [
        {
            targets: 4,
            render: DataTable.render.datetime('Do MMM YYYY')
        }
    ]
});