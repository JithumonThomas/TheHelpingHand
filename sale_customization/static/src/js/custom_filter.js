///** @odoo-module **/
//
//import CustomFilterItem from 'web.CustomFilterItem';
//import { patch } from 'web.utils';
//    const { DatePicker, DateTimePicker } = require('web.DatePickerOwl');
//    const Domain = require('web.Domain');
//    const field_utils = require('web.field_utils');
//    const { useModel } = require('web.Model');
//
//patch(CustomFilterItem.prototype, 'sale_customization.CustomFilterItem', {
//        getPastDate(days){
//            var date = new Date();          // Get current Date
//            date.setDate(date.getDate()-days);
//            return date
//        },
//        convertDate(date) {
//  var yyyy = date.getFullYear().toString();
//  var mm = (date.getMonth()+1).toString();
//  var dd  = date.getDate().toString();
//
//  var mmChars = mm.split('');
//  var ddChars = dd.split('');
//
//  return yyyy + '-' + (mmChars[1]?mm:"0"+mmChars[0]) + '-' + (ddChars[1]?dd:"0"+ddChars[0]);
//},
//    /**
//     * With the `mail` module installed, we want to filter out some of the
//     * available fields in 'Add custom filter' menu (@see CustomFilterItem).
//     * @override
//     */
//    onApply() {
//        const preFilters = this.conditions.map(condition => {
//                const field = this.fields[condition.field];
//                const type = this.FIELD_TYPES[field.type];
//                const operator = this.OPERATORS[type][condition.operator];
//                const descriptionArray = [field.string, operator.description];
//                const domainArray = [];
//                let domainValue;
//                // Field type specifics
//                if ('value' in operator) {
//                    domainValue = [operator.value];
//                    // No description to push here
//                } else if (['date', 'datetime'].includes(type)) {
//                    domainValue = condition.value.map(
//                        val => field_utils.parse[type](val, { type }, { timezone: true })
//                    );
//                    const dateValue = condition.value.map(
//                        val => field_utils.format[type](val, { type }, { timezone: false })
//                    );
//                    descriptionArray.push(`"${dateValue.join(" " + this.env._t("and") + " ")}"`);
//                } else if (type === "selection") {
//                    domainValue = [condition.value];
//                    const formattedValue = field_utils.format[type](condition.value, field);
//                    descriptionArray.push(`"${formattedValue}"`);
//                } else {
//                    domainValue = [condition.value];
//                    descriptionArray.push(`"${condition.value}"`);
//                }
//                // Operator specifics
//                if (operator.symbol === 'between') {
//                    domainArray.push(
//                        [field.name, '>=', domainValue[0]],
//                        [field.name, '<=', domainValue[1]]
//                    );
//                }
//                else if (operator.symbol === "before_3_days") {
//                    domainArray.push(
//                        [field.name, "<=", this.convertDate(this.getPastDate(3))],
//
//                    );
//                }
//                else if (operator.symbol === "before_5_days") {
//                    domainArray.push(
//                        [field.name, "<=", this.convertDate(this.getPastDate(5))],
//
//                    );
//                }
//                else if (operator.symbol === "before_7_days") {
//                    domainArray.push(
//                        [field.name, "<=", this.convertDate(this.getPastDate(7))],
//
//                    );
//                }
//                else if (operator.symbol === "before_10_days") {
//                    domainArray.push(
//                        [field.name, "<=", this.convertDate(this.getPastDate(10))],
//
//                    );
//                }
//                else {
//                    domainArray.push([field.name, operator.symbol, domainValue[0]]);
//                }
//                const preFilter = {
//                    description: descriptionArray.join(" "),
//                    domain: Domain.prototype.arrayToString(domainArray),
//                    type: 'filter',
//                };
//                return preFilter;
//            });
//
//            this.model.dispatch('createNewFilters', preFilters);
//
//            // remove conditions
//            this.conditions.splice(0, this.conditions.length);
//
//            this.addNewCondition();
//
//    },
//});
//
//export default CustomFilterItem;