class Station:
    def __init__(self, id, station_code, global_code, name, old_code, start_date, end_date, type, region, kind, voivo, city, address, N_coor, E_coor):
        self.id = id
        self.station_code = station_code
        self.global_code = global_code
        self.name = name
        self.old_code = old_code
        self.start_date = start_date
        self.end_date = end_date
        self.type = type
        self.region = region
        self.kind = kind
        self.voivo = voivo
        self.city = city
        self.address = address
        self.N_coor = N_coor
        self.E_coor = E_coor

    def __str__(self):
        return (f"Station(id={self.id}, stat_code={self.station_code}, global_code={self.global_code}, "
                f"name={self.name}, old_code={self.old_code}, start_date={self.start_date}, "
                f"end_date={self.end_date}, type={self.type}, region={self.region}, kind={self.kind}, "
                f"voivo={self.voivo}, city={self.city}, address={self.address}, "
                f"N_coor={self.N_coor}, E_coor={self.E_coor})")

    def __repr__(self):
        return (f"Station({self.id}, {self.station_code}, {self.global_code}, {self.name}, "
                f"{self.old_code}, {self.start_date}, {self.end_date}, {self.type}, "
                f"{self.region}, {self.kind}, {self.voivo}, {self.city}, "
                f"{self.address}, {self.N_coor}, {self.E_coor})")

    def __eq__(self, other):
        return self.station_code == other.station_code
