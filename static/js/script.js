function confirmDelete(event, url) {
    event.preventDefault();
    if (confirm('Are you sure you want to delete this item?')) {
        window.location.href = url;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    var deleteButtons = document.querySelectorAll('.deleteButton');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            var confirmDelete = confirm("你確定要刪除這個設定嗎？");
            if (!confirmDelete) {
                event.preventDefault(); // 阻止默認行為，取消刪除操作
            }
        });
    });
});

$(document).ready(function() {
    function formatDate(dateString) {
        // 创建 Date 对象
        var date = new Date(dateString);
        
        // 获取日期部分
        var year = date.getUTCFullYear();
        var month = String(date.getUTCMonth() + 1).padStart(2, '0'); // 月份从0开始
        var day = String(date.getUTCDate()).padStart(2, '0');
        
        // 获取时间部分
        var hours = String(date.getUTCHours()).padStart(1, '0');
        var minutes = String(date.getUTCMinutes()).padStart(2, '0');
        var seconds = String(date.getUTCSeconds()).padStart(2, '0');
        
        // 格式化为 YYYY-MM-DD HH:MM:SS
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        
    }
    function fetchLogData() {
        $.ajax({
            url: '/swipecardlogreturn',
            method: 'GET',
            success: function(data) {
                var tableHtml = '<table border="1" class="table"><tr><th>ID</th><th>Authorization</th><th>Card Number</th><th>Door Name</th><th>Door Status</th><th>Swipe Time</th><th>Username</th></tr>';
                data.forEach(function(logEntry) {
                    // 转换时间格式
                    var formattedSwipetime = formatDate(logEntry.swipetime);

                    tableHtml += '<tr>' +
                        '<td>' + logEntry.id + '</td>' +
                        '<td>' + logEntry.authorization + '</td>' +
                        '<td>' + logEntry.cardnumber + '</td>' +
                        '<td>' + logEntry.doorname + '</td>' +
                        '<td>' + logEntry.doorstatus + '</td>' +
                        '<td>' + formattedSwipetime + '</td>' +
                        '<td>' + logEntry.username + '</td>' +
                        '</tr>';
                });
                tableHtml += '</table>';
                $('div[name="log-container"]').html(tableHtml);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching log data:', error);
            }
        });
    }

    // 每秒检视新的信息
    setInterval(fetchLogData, 1000);

    // 初始加载数据
    fetchLogData();
});
function filterTable() {
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById('searchInput');
    filter = input.value.toUpperCase();
    table = document.getElementById('dataTable');
    tr = table.getElementsByTagName('tr');

    for (i = 1; i < tr.length; i++) { // 从1开始跳过表头
        tr[i].style.display = 'none'; // 默认隐藏行
        td = tr[i].getElementsByTagName('td');
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = '';
                    break; // 一旦找到匹配项就停止进一步检查
                }
            }
        }
    }
}
