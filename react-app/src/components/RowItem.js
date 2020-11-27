import React from 'react';
import './rowitem.scss';

const RowItem = (props) => {

    return (
        <tr>
            <td>
                {props.info[0]}
            </td>
            <td>
                {props.info[1]}
            </td>
            <td>
                {props.info[2]}
            </td>
        </tr>
    );
}

export default RowItem;