import red from '@material-ui/core/colors/red'
import pink from '@material-ui/core/colors/pink'
import green from '@material-ui/core/colors/green'
import {deepPurple, lightBlue} from "@material-ui/core/colors";
import blueGrey from "@material-ui/core/colors/blueGrey";
import grey from "@material-ui/core/colors/grey";
import common from "@material-ui/core/colors/common";
import shadows from "./shadows";
import typography from "./typography";

const themes = [
    {
        id: 'default',
        color: lightBlue[500],
        source: {
            palette: {
                primary: {
                    main: lightBlue[500]
                },
                secondary: {
                    main: deepPurple[500]
                },
                text: {
                    primary: blueGrey[900],
                    secondary: blueGrey[600]
                },
                error: red,
                background: {
                    dark: '#F4F6F8',
                    lightGrey: grey[300],
                    default: common.white,
                    paper: common.white,
                    black: common.black
                }
            },
            shadows,
            typography
        },
    },
    {
        id: 'red',
        color: red[500],
        source: {
            palette: {
                primary: red,
                secondary: pink,
                error: red,
            },
        },
    },
    {
        id: 'green',
        color: green[500],
        source: {
            palette: {
                primary: green,
                secondary: red,
                error: red,
            },
        },
    },
]

export default themes
