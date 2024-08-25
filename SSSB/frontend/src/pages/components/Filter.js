import * as React from 'react';
import dayjs from 'dayjs';
import { useEffect, useState } from 'react';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/Grid';
import OutlinedInput from '@mui/material/OutlinedInput';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Slider from '@mui/material/Slider';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import Switch from '@mui/material/Switch';
import AlarmIcon from '@mui/icons-material/Alarm';
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { styled } from '@mui/system';

import LoadingBox from './LoadingBox';
import Descriptions from './Descriptions';
import LocalDatePicker from './LocalDatePicker';
import SuccessSnackbar from './SimpleSnackbar';
import { fetchRegions, fetchTypes } from '../../Api'
import { fetchSpaceRange, fetchRentRange, fetchFloorRange, fetchCreditRange } from '../../Api'
import { createFilter } from '../../Api'

const FormGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

export default function Filter({ onFilterChange }) {
  const theme = useTheme();

  const [loading, setLoading] = useState(true);
  const [showExpired, setShowExpired] = useState(false);

  const [spaceUnspecified, setSpaceUnspecified] = useState(false);
  const [rentUnspecified, setRentUnspecified] = useState(false);
  const [floorUnspecified, setFloorUnspecified] = useState(false);
  const [creditUnspecified, setCreditUnspecified] = useState(false);

  const [regions, setRegions] = useState([]);
  const [types, setTypes] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState([]);
  const [selectedType, setSelectedType] = useState([]);

  const [spaceMin, setSpaceMin] = useState(0);
  const [spaceMax, setSpaceMax] = useState(200);
  const [spaceRange, setSpaceRange] = useState([0, 100]);

  const [rentMin, setRentMin] = useState(0);
  const [rentMax, setRentMax] = useState(20000);
  const [rentRange, setRentRange] = useState([0, 10000]);

  const [floorMin, setFloorMin] = useState(-5);
  const [floorMax, setFloorMax] = useState(25);
  const [floorRange, setFloorRange] = useState([0, 10000]);

  const [creditMin, setCreditMin] = useState(0);
  const [creditMax, setCreditMax] = useState(2000);
  const [creditRange, setCreditRange] = useState([0, 1000]);

  const [validFromBefore, setValidFromBefore] = useState(null);

  const [electricityIncluded, setEletricityIncluded] = useState("");
  const [summerFree, setSummerFree] = useState("");
  const [max4Years, setMax4Years] = useState("");
  const [shortRent, setShortRent] = useState("");

  // for reminder
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogLoading, setDialogLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [error, setError] = useState(false);
  const [credit, setCredit] = useState("");
  const [successSnackbarOpen, setSuccessSnackbarOpen] = useState(false);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          regionsResponse,
          typesResponse,
          spaceRangeResponse,
          rentRangeResponse,
          floorRangeResponse,
          creditRangeResponse,
        ] = await Promise.all([
          fetchRegions(),
          fetchTypes(),
          fetchSpaceRange(),
          fetchRentRange(),
          fetchFloorRange(),
          fetchCreditRange(),
        ]);
  
        const regions = regionsResponse.data;
        setRegions(regions);
  
        const types = typesResponse.data;
        setTypes(types);
  
        const spaceRange = [spaceRangeResponse.data.min || 0, spaceRangeResponse.data.max || 100];
        setSpaceMin(Math.min(spaceRangeResponse.data.min, 0));
        setSpaceMax(Math.max(spaceRangeResponse.data.max, 150));
        setSpaceRange(spaceRange);
  
        const rentRange = [rentRangeResponse.data.min || 0, rentRangeResponse.data.max || 10000];
        setRentMin(Math.min(rentRangeResponse.data.min,0));
        setRentMax(Math.max(rentRangeResponse.data.max, 25000));
        setRentRange(rentRange);
  
        const floorRange = [floorRangeResponse.data.min || 0, floorRangeResponse.data.max || 10];
        setFloorMin(Math.min(floorRangeResponse.data.min, 0));
        setFloorMax(Math.max(floorRangeResponse.data.max, 30));
        setFloorRange(floorRange);
  
        const creditRange = [creditRangeResponse.data.min || 0, creditRangeResponse.data.max || 1000];
        setCreditMin(Math.min(creditRangeResponse.data.min, 0));
        setCreditMax(Math.max(creditRangeResponse.data.max, 4000));
        setCreditRange(creditRange);
  
      } catch (err) {
        // console.error('Error fetching data:', err);
      } finally {
        setLoading(false); 
      }
    };
  
    fetchData();
  }, []);

 useEffect(() => {
   if (onFilterChange && !loading) {
     onFilterChange({
       selectedRegion,
       selectedType,
       spaceRange,
       rentRange,
       floorRange,
       creditRange,
       spaceUnspecified,
       rentUnspecified,
       floorUnspecified,
       creditUnspecified,
       validFromBefore,
       electricityIncluded,
       summerFree,
       max4Years,
       shortRent,
       showExpired,
     });
    }
  }, [
    selectedRegion,
    selectedType,
    spaceRange,
    rentRange,
    floorRange,
    creditRange,
    spaceUnspecified,
    rentUnspecified,
    floorUnspecified,
    creditUnspecified,
    validFromBefore,
    electricityIncluded,
    summerFree,
    max4Years,
    shortRent,
    showExpired,
    onFilterChange
  ]);

  const handleRegionChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedRegion(value);
  };

  const handleTypeChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedType(value);
  };

  const handleCreateReminder = async () => {
    try {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      setError(!emailRegex.test(email));
      if (!error) {
        const filterDict = {
          "email": email,
          "regions": selectedRegion,
          "types": selectedType,
          "living_space": {
            "min": spaceRange[0],
            "max": spaceRange[1],
          },
          "rent": {
            "min": rentRange[0],
            "max": rentRange[1],
          },
          "floor": {
            "min": floorRange[0],
            "max": floorRange[1],
          },
          "short_rent": shortRent !== "" ? shortRent: null,
          "electricity_include": electricityIncluded !== "" ? electricityIncluded : null,
          "rent_free_june_and_july": summerFree !== "" ? summerFree : null,
          "max_4_years": max4Years !== "" ? max4Years : null,
          "current_credit": credit,
        };
        // console.log(filterDict)
        setDialogLoading(true);
        const response = await createFilter(filterDict);
        setDialogLoading(false);
        setDialogOpen(false);
        setSuccessSnackbarOpen(true);
        setTimeout(() => {
          setSuccessSnackbarOpen(false);
        }, 6000);
      }
    } catch (error) {
        console.error('failed', error);
    }
  };

  return (
    <React.Fragment>
      <LoadingBox loading={loading}>
      <Grid container spacing={2}>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="region">
            Region
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Select
              labelId="demo-multiple-chip-label"
              id="demo-multiple-chip"
              multiple
              displayEmpty
              value={selectedRegion}
              onChange={handleRegionChange}
              input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
              renderValue={(selected) => (
                selected.length === 0 ? (
                  <em>Not Specified</em>
                ) : (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )
              )}
              MenuProps={MenuProps}
              sx={{ flexGrow: 1 }}
            >
              <MenuItem disabled value="">
                <em>Not Specified</em>
              </MenuItem>
              {regions.map((region) => (
                <MenuItem
                  key={region}
                  value={region}
                >
                  {region}
                </MenuItem>
              ))}
            </Select>
            <Button variant="text" sx={{ ml: 2}} onClick={() => {setSelectedRegion([])}}>
              Clear All
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="type">
            Accomodation Type
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Select
              labelId="demo-multiple-chip-label"
              id="demo-multiple-chip"
              multiple
              displayEmpty
              value={selectedType}
              onChange={handleTypeChange}
              input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
              renderValue={(selected) => (
                selected.length === 0 ? (
                  <em>Not Specified</em>
                ) : (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )
              )}
              MenuProps={MenuProps}
              sx={{ flexGrow: 1 }}
            >
              <MenuItem disabled value="">
                <em>Not Specified</em>
              </MenuItem>
              {types.map((type) => (
                <MenuItem
                  key={type}
                  value={type}
                >
                  {type}
                </MenuItem>
              ))}
            </Select>
            <Button variant="text" sx={{ ml: 2}} onClick={() => {setSelectedType([]);}}>
              Clear All
            </Button>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="space">
            Living Space (m²)
            <FormControlLabel 
              control={
                <Switch 
                  checked={spaceUnspecified}
                  onChange={(e) => setSpaceUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Living space range'}
              value={spaceRange}
              onChange={(e) => setSpaceRange(e.target.value)}
              valueLabelDisplay="on"
              min={spaceMin}
              max={spaceMax}
              sx={{ mt: 5 }}
              disabled={spaceUnspecified}
            />

          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="rent">
            Monthly Rent (SEK)

            <FormControlLabel 
              control={
                <Switch 
                  checked={rentUnspecified}
                  onChange={(e) => setRentUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />

          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Rent range'}
              value={rentRange}
              onChange={(e) => setRentRange(e.target.value)}
              valueLabelDisplay="on"
              min={rentMin}
              max={rentMax}
              sx={{ mt: 5 }}
              disabled={rentUnspecified}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="floor">
            Floor
            <FormControlLabel 
              control={
                <Switch 
                  checked={floorUnspecified}
                  onChange={(e) => setFloorUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Floor range'}
              value={floorRange}
              onChange={(e) => setFloorRange(e.target.value)}
              valueLabelDisplay="on"
              min={floorMin}
              max={floorMax}
              sx={{ mt: 5 }}
              disabled={floorUnspecified}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="credit">
            Credit Days Required
            <FormControlLabel 
              control={
                <Switch 
                  checked={creditUnspecified}
                  onChange={(e) => setCreditUnspecified(e.target.checked)}
                  inputProps={{ 'aria-label': 'controlled' }}
                />
              } 
              label="Not Specified" 
              sx={{ ml: 1 }}
            />
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <Slider
              getAriaLabel={() => 'Credit days range'}
              value={creditRange}
              onChange={(e) => setCreditRange(e.target.value)}
              valueLabelDisplay="on"
              min={creditMin}
              max={creditMax}
              sx={{ mt: 5 }}
              disabled={creditUnspecified}
            />
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="valid from before">
            Valid From Before
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 0 }}>
            <LocalDatePicker 
              value={validFromBefore}
              onChange={(value) => setValidFromBefore(value)}
            />
          </Box>
        </FormGrid>

        {/*
        <FormGrid item xs={12}>
          <FormLabel htmlFor="distance to">
            Distance To
          </FormLabel>
          <OutlinedInput
            id="last-name"
            name="last-name"
            type="last-name"
            placeholder="Snow"
            autoComplete="last name"
            required
          />
        </FormGrid>
        */}

        <FormGrid item xs={12}>
          <FormLabel htmlFor="electricity inlcude">
            Electricity Included
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
              value={electricityIncluded}
              onChange={(e) => setEletricityIncluded(e.target.value)}
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="June & July Free">
            June & July Free
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
              value={summerFree}
              onChange={(e) => setSummerFree(e.target.value)}
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="Max 4 Years">
            Max 4 Years
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
              value={max4Years}
              onChange={(e) => setMax4Years(e.target.value)}
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormLabel htmlFor="Short Rent">
            Short Rent
          </FormLabel>
          <Box sx={{ display: 'flex', alignItems: 'center', mx: 2 }}>
            <RadioGroup
              row
              aria-labelledby="demo-row-radio-buttons-group-label"
              name="row-radio-buttons-group"
              value={shortRent}
              onChange={(e) => setShortRent(e.target.value)}
            >
              <FormControlLabel value={true} control={<Radio />} label="Yes" />
              <FormControlLabel value={false} control={<Radio />} label="No" />
              <FormControlLabel value={''} control={<Radio />} label="Not Specified" />
            </RadioGroup>
          </Box>
        </FormGrid>

        <FormGrid item xs={12}>
          <FormControlLabel 
            control={
              <Switch 
                checked={showExpired}
                onChange={(e) => setShowExpired(e.target.checked)}
                inputProps={{ 'aria-label': 'controlled' }}
              />
            } 
            label="Show Expired" 
          />
        </FormGrid>

        <FormGrid item xs={12}>
          <Box sx={{ display: 'flex', mb: 2 }}>
            <Button
              variant="outlined"
              startIcon={<AlarmIcon />}
              onClick={() => setDialogOpen(true)}
            >
              Create Reminder
            </Button>
          </Box>
        </FormGrid>

      </Grid>
      </LoadingBox>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} fullWidth>
        <LoadingBox loading={dialogLoading}>
          <DialogTitle>Create Reminder</DialogTitle>
          <DialogContent>
              <DialogContentText>
                Please enter your email address
              </DialogContentText>
              <TextField
                  autoFocus
                  margin="dense"
                  label="Email address"
                  type="email"
                  fullWidth
                  value={email}
                  error={error}
                  helperText={error ? "Please enter a valid email" : ""}
                  onChange={(e) => setEmail(e.target.value)}
              />
              <DialogContentText>
                Please enter your current credit days
              </DialogContentText>
              <TextField
                  margin="dense"
                  label="Credit days"
                  type="number"
                  fullWidth
                  value={credit}
                  onChange={(e) => setCredit(e.target.value)}
              />
              <DialogContentText>
                Your personal filter
              </DialogContentText>
              <Box sx={{ mt: 1 }}>
                <Descriptions 
                  items={[
                    {
                      "label": "Region",
                      "value": selectedRegion.length > 0 ? selectedRegion.join(", ") : "Not Specified",
                    },
                    {
                      "label": "Accomodation Type",
                      "value": selectedType.length > 0 ? selectedType.join(", ") : "Not Specified",
                    },
                    {
                      "label": "Living Space",
                      "value": `${spaceRange[0]} m² ~ ${spaceRange[1]} m²`,
                    },
                    {
                      "label": "Monthly Rent",
                      "value": `${rentRange[0]} SEK ~ ${rentRange[1]} SEK`,
                    },
                    {
                      "label": "Floor",
                      "value": `${floorRange[0]} ~ ${floorRange[1]}`,
                    },
                    {
                      "label": "Current Credit Days",
                      "value": credit ? `${credit} days`: "Not Specified",
                    },
                    {
                      "label": "Electricity Included",
                      "value": electricityIncluded === "" ? `Not Specified`: (electricityIncluded === "true" ? "Yes": "No"),
                    },
                    {
                      "label": "June & July Free",
                      "value": summerFree === "" ? `Not Specified`: (summerFree === "true" ? "Yes": "No"),
                    },
                    {
                      "label": "Max 4 Years",
                      "value": max4Years === "" ? `Not Specified`: (max4Years === "true" ? "Yes": "No"),
                    },
                    {
                      "label": "Short Rent",
                      "value": shortRent === "" ? `Not Specified`: (shortRent === "true" ? "Yes": "No"),
                    },
                  ]} 
                  column={3} 
                />
              </Box>
          </DialogContent>
          <DialogActions>
              <Button onClick={() => setDialogOpen(false)} color="error">
                  Cancel
              </Button>
              <Button onClick={handleCreateReminder} color="primary">
                  Confirm
              </Button>
          </DialogActions>
        </LoadingBox>
      </Dialog>

      <SuccessSnackbar 
        open={successSnackbarOpen}
        message="Filter created successfully. Please check your email for details."
      />


    </React.Fragment>
  );
}
