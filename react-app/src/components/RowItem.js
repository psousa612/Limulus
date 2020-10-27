import React from 'react';
import './rowitem.scss';

const RowItem = (props) => {
    return (
        <tr>
            <td>
                {props.ranking}
            </td>
            <td>
                {props.username}
            </td>
            <td>
                {props.points}
            </td>
        </tr>
    );
}

export default RowItem;