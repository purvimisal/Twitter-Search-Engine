import Page from 'material-ui-shell/lib/containers/Page'
import React, {useState} from 'react'
import {Container, Grid, makeStyles} from "@material-ui/core";
import Box from "@material-ui/core/Box";
import TextField from "@material-ui/core/TextField";
import InputAdornment from "@material-ui/core/InputAdornment";
import {
    DragHandleOutlined,
    LocationCityOutlined,
    Person,
    SearchRounded
} from "@material-ui/icons";
import Button from "@material-ui/core/Button";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import Avatar from "@material-ui/core/Avatar";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: theme.palette.background.dark,
        minHeight: '100%',
        width: '100%',
        paddingBottom: theme.spacing(3),
        paddingTop: theme.spacing(3)
    },
    rootList: {
        width: '100%',
        backgroundColor: theme.palette.background.paper,
    },
    inline: {
        display: 'inline',
    },
}));

const Home = (callback, deps) => {
    const classes = useStyles();
    const [tweetList, setTweetList] = useState([])
    const [hashtagVal, setHashtagVal] = useState('')
    const [userMentionVal, setUserMentionVal] = useState('')
    const [userLocationVal, setUserLocationVal] = useState('')
    const [usernameVal, setUsernameVal] = useState('')
    const [isFetching, setIsFetching] = useState(false)

    const fetchRequest = () => {
        setIsFetching(true)
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_name: usernameVal,
                user_mention: userMentionVal,
                user_location: userLocationVal,
                hashtag: hashtagVal
            })
        }

        fetch("http://127.0.0.1:5000/searchFields", requestOptions)
            .then(res => res.json())
            .then(
                (result) => {
                    console.log(result)
                    setTweetList(result)
                    setIsFetching(false)
                }
            )

    };

    return (
        <Page className={classes.root}>

            <Container maxWidth={false}>

                <Grid container>
                    <Box
                        xs={12}
                        sm={12}
                        md={12}
                        lg={12}
                        xl={12}
                    >
                        <TextField
                            id="textfield-user-name"
                            label="user-name"
                            style={{margin: 8}}
                            placeholder=""
                            helperText=""
                            margin="normal"
                            value={usernameVal}
                            onChange={e => setUsernameVal(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <Person/>
                                    </InputAdornment>
                                ),
                            }}
                            variant="filled"
                        />
                        <TextField
                            id="textfield-user-location"
                            label="user-location"
                            style={{margin: 8}}
                            placeholder=""
                            helperText=""
                            margin="normal"
                            value={userLocationVal}
                            onChange={e => setUserLocationVal(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <LocationCityOutlined/>
                                    </InputAdornment>
                                ),
                            }}
                            variant="filled"
                        />
                        <TextField
                            id="textfield-user-mention"
                            label="user-mention"
                            style={{margin: 8}}
                            placeholder=""
                            helperText=""
                            margin="normal"
                            value={userMentionVal}
                            onChange={e => setUserMentionVal(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchRounded/>
                                    </InputAdornment>
                                ),
                            }}
                            variant="filled"
                        />
                        <TextField
                            id="textfield-hashtag"
                            label="hashtag"
                            style={{margin: 8}}
                            placeholder=""
                            helperText=""
                            margin="normal"
                            value={hashtagVal}
                            onChange={e => setHashtagVal(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <DragHandleOutlined/>
                                    </InputAdornment>
                                ),
                            }}
                            variant="filled"
                        />
                    </Box>
                    <Box
                        xs={3}
                        sm={3}
                        md={3}
                        lg={3}
                        xl={3}
                    >
                        <Button variant="contained" color="secondary" style={{margin: 8, marginLeft: 20}}
                                onClick={fetchRequest} disabled={isFetching}>
                            Search
                        </Button>
                    </Box>
                    <Box
                        xs={12}
                        sm={12}
                        md={12}
                        lg={12}
                        xl={12}
                        width={1}
                    >
                        <List className={classes.rootList}>
                            {
                                tweetList.map((item, idx) => {
                                    return (
                                        <div id={"list-child-" + idx}>
                                            <ListItem alignItems="flex-start">
                                                <ListItemAvatar>
                                                    <Avatar alt={item.user_screen_name}
                                                            src="/static/images/avatar/1.jpg"
                                                    />
                                                </ListItemAvatar>
                                                <ListItemText
                                                    primary={item.user_name}
                                                    secondary={
                                                        <React.Fragment>
                                                            <Typography
                                                                component="span"
                                                                variant="body2"
                                                                className={classes.inline}
                                                                color="textPrimary"
                                                            >
                                                                {item.text}
                                                            </Typography>
                                                            {" ~ " + item.user_screen_name}
                                                        </React.Fragment>
                                                    }
                                                />
                                            </ListItem>
                                            <Divider variant="inset" component="li"/>
                                        </div>)
                                })
                            }
                        </List>
                    </Box>
                </Grid>
            </Container>
        </Page>
    )
}
export default Home

