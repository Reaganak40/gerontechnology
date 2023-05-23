import { _adapters } from 'chart.js';
import dayjs from 'dayjs';
import CustomParseFormat from 'dayjs/plugin/customParseFormat.js';
import AdvancedFormat from 'dayjs/plugin/advancedFormat.js';
import QuarterOfYear from 'dayjs/plugin/quarterOfYear.js';
import LocalizedFormat from 'dayjs/plugin/localizedFormat.js';
import isoWeek from 'dayjs/plugin/isoWeek.js';

dayjs.extend(AdvancedFormat);
dayjs.extend(QuarterOfYear);
dayjs.extend(LocalizedFormat);
dayjs.extend(CustomParseFormat);
dayjs.extend(isoWeek);
var FORMATS = {
  datetime: 'MMM D, YYYY, h:mm:ss a',
  millisecond: 'h:mm:ss.SSS a',
  second: 'h:mm:ss a',
  minute: 'h:mm a',
  hour: 'hA',
  day: 'MMM D',
  week: 'll',
  month: 'MMM YYYY',
  quarter: '[Q]Q - YYYY',
  year: 'YYYY'
};
_adapters._date.override({
  //_id: 'dayjs', //DEBUG,
  formats: function formats() {
    return FORMATS;
  },
  parse: function parse(value, format) {
    var valueType = typeof value;
    if (value === null || valueType === 'undefined') {
      return null;
    }
    if (valueType === 'string' && typeof format === 'string') {
      return dayjs(value, format).isValid() ? dayjs(value, format).valueOf() : null;
    } else if (!(value instanceof dayjs)) {
      return dayjs(value).isValid() ? dayjs(value).valueOf() : null;
    }
    return null;
  },
  format: function format(time, _format) {
    return dayjs(time).format(_format);
  },
  add: function add(time, amount, unit) {
    return dayjs(time).add(amount, unit).valueOf();
  },
  diff: function diff(max, min, unit) {
    return dayjs(max).diff(dayjs(min), unit);
  },
  startOf: function startOf(time, unit, weekday) {
    if (unit === 'isoWeek') {
      // Ensure that weekday has a valid format
      //const formattedWeekday
      var validatedWeekday = typeof weekday === 'number' && weekday > 0 && weekday < 7 ? weekday : 1;
      return dayjs(time).isoWeekday(validatedWeekday).startOf('day').valueOf();
    }
    return dayjs(time).startOf(unit).valueOf();
  },
  endOf: function endOf(time, unit) {
    return dayjs(time).endOf(unit).valueOf();
  }
});
//# sourceMappingURL=chartjs-adapter-dayjs-4.esm.js.map
