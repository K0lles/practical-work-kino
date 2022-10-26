function parseISOLocal(s) {
  let b = s.split(/\D/);
  return new Date(b[0], b[1]-1, b[2], b[3], b[4], b[5]);
}

function padTo2Digits(num) {
  return num.toString().padStart(2, '0');
}

function formatDate(date) {
  return [
    date.getFullYear(),
    padTo2Digits(date.getMonth() + 1),
    padTo2Digits(date.getDate()),
  ].join('-');
}

function parseToFullMinutes(minute) {
    if (String(minute).length == 1) {
        return String(minute) + "0"
    }

    return minute

}

function scheduleParse(data) {
    let dateNumbers = ['Неділя', 'Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П`ятниця', 'Субота']
    let dateMonths = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень']
    let schedule = $('#schedule');
    schedule.empty();
    for (let date = 0; date < data['dates'].length; date++) {
        let contentTable = `<div class="row" style="margin-top: 4%;">
                                <h5>${parseISOLocal(data['dates'][date]).getDate()} ${dateMonths[parseISOLocal(data['dates'][date]).getMonth()]}, ${dateNumbers[parseISOLocal(data['dates'][date]).getDay()]}</h5>
                                <table class="col-12 table-bordered" style="border: solid orange 2px;">
                                    <thead class="text-center">
                                        <td>Час</td>
                                        <td>Фільм</td>
                                        <td>Зал</td>
                                        <td>Ціна</td>
                                        <td style="color: firebrick">Бронювати</td>
                                    </thead>
                                    <tbody>`;
        for (let session = 0; session < data['sessions'].length; session++) {
            if (formatDate(parseISOLocal(data['dates'][date])) == formatDate(parseISOLocal(data['sessions'][session]['fields']['date']))) {
                contentTable += `<tr class="text-center">
                                    <td>${parseISOLocal(data['sessions'][session]['fields']['date']).getHours()+3}:${parseToFullMinutes(parseISOLocal(data['sessions'][session]['fields']['date']).getMinutes())}</td>
                                    <td>${data['sessions'][session]['fields']['movie']}</td>
                                    <td>${data['sessions'][session]['fields']['hall']}</td>
                                    <td>${data['sessions'][session]['fields']['price']}</td>
                                    <td><a href="/movie/book/${data['sessions'][session]['pk']}" style="text-decoration: none">
                                            <img src="/static/movie/logos/ticket.png" height="15px" width="15px">
                                        </a></td>
                                 </tr>`
            }
        }
        contentTable += `</tbody>
                         </table>
                         </div>`
        schedule.append(contentTable);
    }
  }
