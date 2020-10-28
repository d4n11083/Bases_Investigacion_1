import React from 'react';
import { List,Image, Header } from "semantic-ui-react";

export const Users = ( { users } ) => {


    return (
        <List horizontal ordered relaxed>
            {users.map(user=>{
                return(
                    <List.Item key={user.id}>
                        <Image avatar src='https://react.semantic-ui.com/images/avatar/small/tom.jpg' />
                        <List.Content>
                        <List.Header as='a'>{user.name}</List.Header>
                        <List.Description>
                        Vive en {' '}
                        <a>
                            <b>{user.location}</b>
                        </a>{' '}

                        su ID es {' '}
                        <a>
                            <b>{user.id}</b>
                        </a>{' '}

                        </List.Description>
                    </List.Content>
                    </List.Item>
                )
            })}
        </List>
    )
};